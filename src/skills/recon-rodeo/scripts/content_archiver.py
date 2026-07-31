#!/usr/bin/env python3
"""
ospo :: content archiver

Capture public web content with Playwright, yt-dlp, and gallery-dl. Each capture
gets a dedicated directory, structured tool records, SHA-256 file inventory,
and a final JSON manifest.

This tool performs read-only retrieval. Operators remain responsible for
authorization, applicable platform terms, retention rules, and lawful use.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from collections.abc import Iterator, Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit, urlunsplit

from osint_common import UnsafeTargetError, validate_public_url

try:
    from playwright.async_api import Browser, Error as PlaywrightError
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError
    from playwright.async_api import async_playwright

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

CaptureStatus = Literal["success", "partial", "failed", "skipped", "timeout"]
JsonDict = dict[str, Any]

MANIFEST_FILENAME = "manifest.json"
CAPTURE_SCHEMA_VERSION = "1.0"
MAX_LOG_BYTES = 32_768
DEFAULT_TOOL_TIMEOUT_SECONDS = 300
DEFAULT_PAGE_TIMEOUT_MS = 30_000
DEFAULT_SETTLE_DELAY_MS = 1_500
ALLOWED_SCHEMES = frozenset({"http", "https"})


class ArchiveError(RuntimeError):
    """Raised when a capture request or output workspace is invalid."""


@dataclass(frozen=True)
class ArchivePolicy:
    """Capture policy controlling network scope and bounded tool execution."""

    allow_private_hosts: bool = False
    allow_external_downloaders: bool = False
    tool_timeout_seconds: int = DEFAULT_TOOL_TIMEOUT_SECONDS
    page_timeout_ms: int = DEFAULT_PAGE_TIMEOUT_MS
    settle_delay_ms: int = DEFAULT_SETTLE_DELAY_MS
    max_concurrent_archives: int = 2

    def __post_init__(self) -> None:
        if self.tool_timeout_seconds <= 0:
            raise ValueError("tool_timeout_seconds must be positive.")
        if self.page_timeout_ms <= 0:
            raise ValueError("page_timeout_ms must be positive.")
        if self.settle_delay_ms < 0:
            raise ValueError("settle_delay_ms must not be negative.")
        if self.max_concurrent_archives <= 0:
            raise ValueError("max_concurrent_archives must be positive.")


@dataclass(frozen=True)
class ValidatedURL:
    """A normalized, policy-checked public HTTP(S) URL."""

    original: str
    normalized: str
    hostname: str
    scheme: str


@dataclass
class ToolCapture:
    """One independently executed capture method and its artifacts."""

    tool: str
    status: CaptureStatus
    started_at_utc: str
    completed_at_utc: str
    files: list[JsonDict] = field(default_factory=list)
    return_code: int | None = None
    reason: str | None = None
    stderr: str | None = None
    stdout: str | None = None
    metadata: JsonDict = field(default_factory=dict)


def utc_now() -> str:
    """Return a canonical UTC timestamp with second precision."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(filepath: Path) -> str:
    """Compute the SHA-256 digest of a regular file."""
    digest = hashlib.sha256()

    with filepath.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def _has_tool(name: str) -> bool:
    """Return whether an executable is currently resolvable on PATH."""
    return shutil.which(name) is not None


def _truncate_output(raw: bytes) -> str:
    """Decode bounded subprocess output for a JSON capture record."""
    if len(raw) > MAX_LOG_BYTES:
        raw = raw[:MAX_LOG_BYTES] + b"\n[output truncated]\n"
    return raw.decode("utf-8", errors="replace")


def _is_link_or_reparse(path: Path) -> bool:
    """Return whether path is a symlink, Windows junction, or reparse point."""
    result = path.lstat()
    attributes = getattr(result, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(result.st_mode) or bool(attributes & reparse_flag)


def _is_within(path: Path, root: Path) -> bool:
    """Return whether already-resolved path is contained by root."""
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _safe_regular_files(root: Path) -> Iterator[Path]:
    """Yield regular files below root without traversing links or reparse points."""
    resolved_root = root.resolve(strict=True)
    if _is_link_or_reparse(resolved_root):
        raise ArchiveError(f"Refusing symlink or reparse-point directory: {root}")

    pending = [resolved_root]
    while pending:
        directory = pending.pop()

        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)

                if _is_link_or_reparse(path):
                    raise ArchiveError(
                        f"Refusing symlink or reparse-point capture artifact: {path}"
                    )

                resolved_path = path.resolve(strict=True)
                if not _is_within(resolved_path, resolved_root):
                    raise ArchiveError(
                        f"Capture artifact escapes output directory: {path}"
                    )

                if entry.is_dir(follow_symlinks=False):
                    pending.append(resolved_path)
                elif entry.is_file(follow_symlinks=False):
                    yield resolved_path


def _atomic_write_json(path: Path, value: JsonDict) -> None:
    """Atomically write a UTF-8 JSON document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, indent=2, sort_keys=True) + "\n"

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary_path = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())

    try:
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _is_private_or_local_host(hostname: str) -> bool:
    """Reject hostname forms that are plainly local without DNS resolution."""
    normalized = hostname.casefold().rstrip(".")

    if normalized in {"localhost", "localhost.localdomain"}:
        return True
    if normalized.endswith(".localhost"):
        return True

    try:
        import ipaddress

        address = ipaddress.ip_address(normalized)
    except ValueError:
        return False

    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def validate_url(url: str, *, allow_private_hosts: bool = False) -> ValidatedURL:
    """Validate a capture URL and reject non-web or plainly local destinations.

    DNS rebinding and redirects require stricter network-layer controls than
    application validation alone. Use an egress firewall or isolated browser
    profile for hostile or untrusted URLs.
    """
    if not isinstance(url, str) or not url.strip():
        raise ArchiveError("URL must be a non-empty string.")

    original = url.strip()
    parsed = urlsplit(original)

    if parsed.scheme.casefold() not in ALLOWED_SCHEMES:
        raise ArchiveError("Only http:// and https:// URLs are supported.")
    if not parsed.hostname:
        raise ArchiveError("URL must include a hostname.")
    if parsed.username or parsed.password:
        raise ArchiveError("URLs containing embedded credentials are not accepted.")

    hostname = parsed.hostname.casefold().rstrip(".")
    if not allow_private_hosts and _is_private_or_local_host(hostname):
        raise ArchiveError(
            "Refusing localhost, private, link-local, or special-use IP targets. "
            "Use an isolated environment and explicit policy override if required."
        )

    normalized = urlunsplit(
        (
            parsed.scheme.casefold(),
            parsed.netloc,
            parsed.path or "/",
            parsed.query,
            "",
        )
    )
    return ValidatedURL(
        original=original,
        normalized=normalized,
        hostname=hostname,
        scheme=parsed.scheme.casefold(),
    )


class ContentArchiver:
    """Multi-method public-content archiver with final package inventory."""

    def __init__(
        self,
        output_dir: str | Path = "./captures",
        *,
        policy: ArchivePolicy | None = None,
    ) -> None:
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.output_dir.is_dir() or _is_link_or_reparse(self.output_dir):
            raise ArchiveError(
                f"Output directory must be a non-link directory: {self.output_dir}"
            )

        self.policy = policy or ArchivePolicy()
        self._archive_semaphore = asyncio.Semaphore(
            self.policy.max_concurrent_archives
        )

    def _capture_dir(self, url: ValidatedURL) -> Path:
        """Create a collision-resistant, URL-bound capture directory."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        url_digest = hashlib.sha256(url.normalized.encode("utf-8")).hexdigest()[:16]
        capture_name = f"{timestamp}_{url.hostname}_{url_digest}"
        capture_name = capture_name.replace(":", "_")

        for sequence in range(1, 10_000):
            suffix = "" if sequence == 1 else f"_{sequence:03d}"
            candidate = self.output_dir / f"{capture_name}{suffix}"
            try:
                candidate.mkdir(mode=0o750)
            except FileExistsError:
                continue
            return candidate

        raise ArchiveError("Could not allocate a unique capture directory.")

    @staticmethod
    def _tool_directory(capture_dir: Path, name: str) -> Path:
        """Create a dedicated output directory for one capture mechanism."""
        directory = capture_dir / name
        directory.mkdir(mode=0o750, exist_ok=False)
        return directory

    def _hash_directory(self, directory: Path) -> list[JsonDict]:
        """Return a deterministic SHA-256 inventory of regular capture artifacts."""
        return [
            {
                "file": file.relative_to(directory).as_posix(),
                "sha256": sha256_file(file),
                "bytes": file.stat().st_size,
            }
            for file in sorted(
                _safe_regular_files(directory),
                key=lambda path: path.relative_to(directory).as_posix(),
            )
        ]

    async def _run_tool(
        self,
        *,
        tool: str,
        command: Sequence[str],
        output_directory: Path,
    ) -> ToolCapture:
        """Execute a downloader with bounded runtime and captured diagnostics."""
        started_at = utc_now()

        if not _has_tool(tool):
            return ToolCapture(
                tool=tool,
                status="skipped",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                reason="executable_not_found",
            )

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(output_directory),
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.policy.tool_timeout_seconds,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.communicate()
            return ToolCapture(
                tool=tool,
                status="timeout",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                reason=(
                    f"exceeded_timeout_seconds:{self.policy.tool_timeout_seconds}"
                ),
            )
        except OSError as exc:
            return ToolCapture(
                tool=tool,
                status="failed",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                reason=f"process_execution_error:{exc}",
            )

        files = self._hash_directory(output_directory)
        status: CaptureStatus
        if process.returncode == 0:
            status = "success"
        elif files:
            status = "partial"
        else:
            status = "failed"

        return ToolCapture(
            tool=tool,
            status=status,
            started_at_utc=started_at,
            completed_at_utc=utc_now(),
            return_code=process.returncode,
            files=files,
            stdout=_truncate_output(stdout),
            stderr=_truncate_output(stderr),
        )

    async def download_ytdlp(
        self,
        url: ValidatedURL,
        capture_dir: Path,
    ) -> ToolCapture:
        """Capture available audio/video and metadata via yt-dlp."""
        media_dir = self._tool_directory(capture_dir, "yt-dlp")

        command = [
            "yt-dlp",
            "--no-playlist",
            "--no-progress",
            "--restrict-filenames",
            "--paths",
            str(media_dir),
            "--output",
            "%(id)s_%(title).150B.%(ext)s",
            "--write-info-json",
            "--write-thumbnail",
            "--write-description",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "all",
            "--",
            url.normalized,
        ]
        return await self._run_tool(
            tool="yt-dlp",
            command=command,
            output_directory=media_dir,
        )

    async def download_gallery_dl(
        self,
        url: ValidatedURL,
        capture_dir: Path,
    ) -> ToolCapture:
        """Capture available image-gallery content and metadata via gallery-dl."""
        images_dir = self._tool_directory(capture_dir, "gallery-dl")

        command = [
            "gallery-dl",
            "--destination",
            str(images_dir),
            "--write-metadata",
            "--",
            url.normalized,
        ]
        return await self._run_tool(
            tool="gallery-dl",
            command=command,
            output_directory=images_dir,
        )

    async def _capture_screenshot(
        self,
        url: ValidatedURL,
        capture_dir: Path,
    ) -> ToolCapture:
        """Capture a full-page PNG and navigation metadata through Playwright."""
        started_at = utc_now()

        if not HAS_PLAYWRIGHT:
            return ToolCapture(
                tool="playwright",
                status="skipped",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                reason="python_package_not_installed",
            )

        screenshot_dir = self._tool_directory(capture_dir, "playwright")
        screenshot_path = screenshot_dir / "page.png"
        browser: Browser | None = None

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    ignore_https_errors=False,
                    java_script_enabled=True,
                )
                page = await context.new_page()
                page.set_default_navigation_timeout(self.policy.page_timeout_ms)
                page.set_default_timeout(self.policy.page_timeout_ms)

                async def public_requests_only(route):
                    if self.policy.allow_private_hosts:
                        await route.continue_()
                        return
                    try:
                        await asyncio.to_thread(
                            validate_public_url,
                            route.request.url,
                        )
                    except (UnsafeTargetError, ValueError):
                        await route.abort("blockedbyclient")
                        return
                    await route.continue_()

                await page.route("**/*", public_requests_only)

                response = await page.goto(
                    url.normalized,
                    wait_until="domcontentloaded",
                )

                if self.policy.settle_delay_ms:
                    await page.wait_for_timeout(self.policy.settle_delay_ms)

                title = await page.title()
                final_url = page.url
                if not self.policy.allow_private_hosts:
                    await asyncio.to_thread(validate_public_url, final_url)
                await page.screenshot(
                    path=str(screenshot_path),
                    full_page=True,
                    animations="disabled",
                )
                await context.close()

            return ToolCapture(
                tool="playwright",
                status="success",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                files=self._hash_directory(screenshot_dir),
                metadata={
                    "requested_url": url.normalized,
                    "final_url": final_url,
                    "page_title": title,
                    "response_status": response.status if response else None,
                    "wait_until": "domcontentloaded",
                    "settle_delay_ms": self.policy.settle_delay_ms,
                    "viewport": {"width": 1920, "height": 1080},
                },
            )
        except PlaywrightTimeoutError as exc:
            return ToolCapture(
                tool="playwright",
                status="timeout",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                reason=str(exc),
            )
        except PlaywrightError as exc:
            return ToolCapture(
                tool="playwright",
                status="failed",
                started_at_utc=started_at,
                completed_at_utc=utc_now(),
                reason=str(exc),
            )
        finally:
            if browser is not None:
                await browser.close()

    async def archive(self, url: str) -> JsonDict:
        """Run independent capture mechanisms and create a final manifest."""
        validated_url = validate_url(
            url,
            allow_private_hosts=self.policy.allow_private_hosts,
        )

        async with self._archive_semaphore:
            capture_dir = self._capture_dir(validated_url)
            started_at = utc_now()

            try:
                downloader_results = (
                    (
                        self.download_ytdlp(validated_url, capture_dir),
                        self.download_gallery_dl(validated_url, capture_dir),
                    )
                    if self.policy.allow_external_downloaders
                    else (
                        asyncio.sleep(
                            0,
                            result=ToolCapture(
                                tool="yt-dlp",
                                status="skipped",
                                started_at_utc=started_at,
                                completed_at_utc=utc_now(),
                                reason="external_downloaders_require_explicit_opt_in",
                            ),
                        ),
                        asyncio.sleep(
                            0,
                            result=ToolCapture(
                                tool="gallery-dl",
                                status="skipped",
                                started_at_utc=started_at,
                                completed_at_utc=utc_now(),
                                reason="external_downloaders_require_explicit_opt_in",
                            ),
                        ),
                    )
                )
                results = await asyncio.gather(
                    self._capture_screenshot(validated_url, capture_dir),
                    *downloader_results,
                )
            except Exception as exc:
                # gather should normally contain tool failures as records; this is
                # reserved for unexpected orchestration faults.
                raise ArchiveError(f"Capture orchestration failed: {exc}") from exc

            captures = [asdict(result) for result in results]
            inventory = [
                {
                    "file": file.relative_to(capture_dir).as_posix(),
                    "sha256": sha256_file(file),
                    "bytes": file.stat().st_size,
                }
                for file in sorted(
                    _safe_regular_files(capture_dir),
                    key=lambda path: path.relative_to(capture_dir).as_posix(),
                )
                if file.name != MANIFEST_FILENAME
            ]

            status_counts = {
                status: sum(
                    1 for capture in captures if capture["status"] == status
                )
                for status in ("success", "partial", "failed", "timeout", "skipped")
            }

            manifest: JsonDict = {
                "schema_version": CAPTURE_SCHEMA_VERSION,
                "requested_url": validated_url.original,
                "normalized_url": validated_url.normalized,
                "hostname": validated_url.hostname,
                "capture_started_at_utc": started_at,
                "capture_completed_at_utc": utc_now(),
                "capture_directory": str(capture_dir),
                "policy": {
                    "allow_private_hosts": self.policy.allow_private_hosts,
                    "tool_timeout_seconds": self.policy.tool_timeout_seconds,
                    "page_timeout_ms": self.policy.page_timeout_ms,
                    "settle_delay_ms": self.policy.settle_delay_ms,
                },
                "captures": captures,
                "inventory": {
                    "hash_algorithm": "sha256",
                    "file_count": len(inventory),
                    "total_bytes": sum(item["bytes"] for item in inventory),
                    "files": inventory,
                },
                "summary": {
                    "tool_status_counts": status_counts,
                    "successful_tools": status_counts["success"],
                    "total_tools": len(captures),
                    "statement": (
                        f"{status_counts['success']}/{len(captures)} "
                        "capture methods completed successfully"
                    ),
                },
                "limitations": [
                    "A successful retrieval does not establish authorship, accuracy, "
                    "or original publication time.",
                    "Platform output can differ by region, authentication, account, "
                    "device, or time of retrieval.",
                    "The final manifest is not included in its own file inventory.",
                ],
            }

            _atomic_write_json(capture_dir / MANIFEST_FILENAME, manifest)
            return manifest


async def _archive_many(
    archiver: ContentArchiver,
    urls: Sequence[str],
) -> list[tuple[str, JsonDict | ArchiveError]]:
    """Archive multiple URLs while retaining a result for every supplied URL."""
    tasks = [asyncio.create_task(archiver.archive(url)) for url in urls]
    raw_results = await asyncio.gather(*tasks, return_exceptions=True)

    results: list[tuple[str, JsonDict | ArchiveError]] = []
    for url, result in zip(urls, raw_results, strict=True):
        if isinstance(result, ArchiveError):
            results.append((url, result))
        elif isinstance(result, Exception):
            results.append((url, ArchiveError(str(result))))
        else:
            results.append((url, result))
    return results


async def main() -> int:
    """Run the content archiver command-line interface."""
    parser = argparse.ArgumentParser(description="Archive public web content")
    parser.add_argument("urls", nargs="+", help="HTTP(S) URLs to archive")
    parser.add_argument(
        "--output",
        "-o",
        default="./captures",
        help="Capture parent directory",
    )
    parser.add_argument(
        "--allow-private-hosts",
        action="store_true",
        help="Permit localhost/private-IP URLs; use only in an isolated environment",
    )
    parser.add_argument(
        "--allow-external-downloaders",
        action="store_true",
        help=(
            "Enable yt-dlp and gallery-dl only inside an egress-restricted "
            "environment; their internal redirects cannot be policy-pinned"
        ),
    )
    parser.add_argument(
        "--tool-timeout",
        type=int,
        default=DEFAULT_TOOL_TIMEOUT_SECONDS,
        help="Maximum seconds per downloader",
    )
    parser.add_argument(
        "--page-timeout-ms",
        type=int,
        default=DEFAULT_PAGE_TIMEOUT_MS,
        help="Playwright navigation timeout in milliseconds",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=2,
        help="Maximum simultaneous URL archives",
    )
    args = parser.parse_args()

    try:
        policy = ArchivePolicy(
            allow_private_hosts=args.allow_private_hosts,
            allow_external_downloaders=args.allow_external_downloaders,
            tool_timeout_seconds=args.tool_timeout,
            page_timeout_ms=args.page_timeout_ms,
            max_concurrent_archives=args.concurrency,
        )
        archiver = ContentArchiver(args.output, policy=policy)
    except (ArchiveError, ValueError) as exc:
        print(f"Archiver configuration failed: {exc}", file=sys.stderr)
        return 2

    results = await _archive_many(archiver, args.urls)
    failures = 0

    for url, result in results:
        if isinstance(result, ArchiveError):
            failures += 1
            print(f"{url} -> failed: {result}", file=sys.stderr)
            continue

        summary = result["summary"]
        print(
            f"{url} -> {summary['statement']} -> "
            f"{result['capture_directory']}"
        )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
