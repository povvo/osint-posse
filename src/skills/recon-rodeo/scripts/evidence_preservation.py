#!/usr/bin/env python3
"""ospo acquisition receipt pipeline.

Captures and hashes public web material. The receipt records acquisition
parameters and byte identity; it is not a custody-event chain.

Capabilities:
    - Full-page screenshots via Playwright
    - HTML/DOM capture
    - SHA-256 hashing of all artefacts
    - WARC file creation (ISO 28500)
    - Wayback Machine submission
    - Acquisition receipt generation

Usage:
    from scripts.evidence_preservation import EvidencePreserver
    ep = EvidencePreserver(output_dir="./evidence")
    result = await ep.preserve("https://example.com")
"""

import asyncio
import base64
import hashlib
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Optional

from osint_common import PublicSourceClient, UnsafeTargetError, slugify, validate_public_url

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    from warcio.warcwriter import WARCWriter
    from warcio.statusandheaders import StatusAndHeaders
    HAS_WARCIO = True
except ImportError:
    HAS_WARCIO = False

try:
    import waybackpy
    HAS_WAYBACK = True
except ImportError:
    HAS_WAYBACK = False

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class EvidencePreserver:
    """Capture public web material and issue a verifiable acquisition receipt."""

    def __init__(
        self,
        output_dir: str = "./evidence",
        analyst_id: str = "green-ink",
        max_response_bytes: int = 10 * 1024 * 1024,
        timeout_seconds: int = 30,
    ):
        self.output_dir = Path(output_dir)
        self.analyst_id = analyst_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.http = PublicSourceClient(
            timeout=timeout_seconds,
            max_bytes=max_response_bytes,
            max_redirects=5,
            min_interval_seconds=1.0,
        )

    @staticmethod
    def sha256_file(filepath: Path) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def sha256_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _case_dir(self, url: str) -> Path:
        """Create a timestamped directory for this capture."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        safe_name = slugify(url.replace("https://", "").replace("http://", ""), 60)
        return Path(tempfile.mkdtemp(prefix=f"{ts}_{safe_name}_", dir=self.output_dir))

    async def capture_screenshot(self, url: str, case_dir: Path) -> Optional[dict]:
        """Full-page screenshot via Playwright."""
        if not HAS_PLAYWRIGHT:
            return {"type": "screenshot", "status": "skipped", "reason": "playwright not installed"}

        screenshot_path = case_dir / "screenshot.png"
        try:
            validate_public_url(url)
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(viewport={"width": 1920, "height": 1080})

                async def public_requests_only(route):
                    try:
                        await asyncio.to_thread(validate_public_url, route.request.url)
                    except (UnsafeTargetError, ValueError):
                        await route.abort("blockedbyclient")
                        return
                    await route.continue_()

                await page.route("**/*", public_requests_only)
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.screenshot(path=str(screenshot_path), full_page=True)
                title = await page.title()
                await browser.close()

            file_hash = self.sha256_file(screenshot_path)
            return {
                "type": "screenshot",
                "status": "captured",
                "path": str(screenshot_path),
                "sha256": file_hash,
                "page_title": title,
                "bytes": screenshot_path.stat().st_size,
            }
        except Exception as e:
            return {"type": "screenshot", "status": "failed", "error": str(e)}

    async def capture_html(self, url: str, case_dir: Path) -> Optional[dict]:
        """Bounded HTML capture through the shared redirect- and DNS-safe client."""
        html_path = case_dir / "page.html"
        headers_path = case_dir / "response_headers.json"
        try:
            response = await asyncio.to_thread(self.http.get, url, retries=0)
            if response.get("error"):
                raise RuntimeError(str(response["error"]))
            encoded_content = response.get("content_base64")
            if not isinstance(encoded_content, str):
                raise RuntimeError("HTTP client did not preserve the original response bytes")
            html_bytes = base64.b64decode(encoded_content, validate=True)
            if self.sha256_bytes(html_bytes) != response.get("content_sha256"):
                raise RuntimeError("HTTP response byte digest does not match the captured payload")
            html_path.write_bytes(html_bytes)
            headers_path.write_text(json.dumps(response.get("headers", {}), indent=2), encoding="utf-8")

            return {
                "type": "html",
                "status": "captured",
                "path": str(html_path),
                "sha256": self.sha256_bytes(html_bytes),
                "status_code": response.get("status_code"),
                "bytes": len(html_bytes),
                "headers_path": str(headers_path),
                "final_url": response.get("url"),
                "redirected": response.get("url") != url,
                "response_headers": response.get("headers", {}),
            }
        except Exception as e:
            return {"type": "html", "status": "failed", "error": str(e)}

    def create_warc(
        self,
        url: str,
        case_dir: Path,
        html_path: Path,
        capture: dict,
    ) -> Optional[dict]:
        """Create ISO 28500 WARC file from captured HTML."""
        if not HAS_WARCIO:
            return {"type": "warc", "status": "skipped", "reason": "warcio not installed"}
        if not html_path.exists():
            return {"type": "warc", "status": "skipped", "reason": "no HTML capture to archive"}

        warc_path = case_dir / "capture.warc.gz"
        try:
            with open(warc_path, "wb") as fh:
                writer = WARCWriter(fh, gzip=True)
                with open(html_path, "rb") as payload:
                    status_code = capture.get("status_code")
                    response_headers = capture.get("response_headers", {})
                    if not isinstance(status_code, int):
                        return {
                            "type": "warc",
                            "status": "skipped",
                            "reason": "capture has no HTTP status",
                        }
                    headers = StatusAndHeaders(
                        str(status_code),
                        [(str(name), str(value)) for name, value in response_headers.items()],
                        protocol="HTTP/1.1",
                    )
                    record = writer.create_warc_record(
                        str(capture.get("final_url") or url),
                        "response",
                        payload=payload,
                        http_headers=headers,
                    )
                    writer.write_record(record)

            return {
                "type": "warc",
                "status": "created",
                "path": str(warc_path),
                "sha256": self.sha256_file(warc_path),
                "bytes": warc_path.stat().st_size,
            }
        except Exception as e:
            return {"type": "warc", "status": "failed", "error": str(e)}

    def submit_wayback(self, url: str) -> dict:
        """Submit URL to Wayback Machine for independent corroboration."""
        if not HAS_WAYBACK:
            return {"type": "wayback", "status": "skipped", "reason": "waybackpy not installed"}

        try:
            validate_public_url(url)
            user_agent = "green-ink/0.1 (evidence-preservation)"
            save_api = waybackpy.WaybackMachineSaveAPI(url, user_agent)
            save_api.save()
            return {
                "type": "wayback",
                "status": "submitted",
                "archive_url": save_api.archive_url,
                "timestamp": save_api.timestamp().isoformat() if hasattr(save_api, 'timestamp') else None,
            }
        except Exception as e:
            return {"type": "wayback", "status": "failed", "error": str(e)}

    async def preserve(self, url: str, submit_to_wayback: bool = True) -> dict:
        """Full evidence preservation pipeline for a single URL."""
        validate_public_url(url)
        case_dir = self._case_dir(url)
        capture_utc = datetime.now(timezone.utc).isoformat()

        artefacts = []

        # 1. Screenshot
        screenshot = await self.capture_screenshot(url, case_dir)
        artefacts.append(screenshot)

        # 2. HTML capture
        html_result = await self.capture_html(url, case_dir)
        artefacts.append(html_result)

        # 3. WARC creation
        html_path = case_dir / "page.html"
        warc_result = self.create_warc(url, case_dir, html_path, html_result or {})
        artefacts.append(warc_result)

        # 4. Wayback Machine submission
        if submit_to_wayback:
            wb_result = self.submit_wayback(url)
            artefacts.append(wb_result)

        # 5. Acquisition receipt. This proves byte identity after capture, not custody.
        try:
            package_version = metadata.version("osint-posse")
        except metadata.PackageNotFoundError:
            package_version = "0.1.0"
        receipt = {
            "schema_version": "1.1",
            "record_type": "acquisition_receipt",
            "case_directory": str(case_dir),
            "requested_url": url,
            "final_url": (html_result or {}).get("final_url"),
            "redirected": (html_result or {}).get("redirected"),
            "response_status": (html_result or {}).get("status_code"),
            "response_headers": (html_result or {}).get("response_headers", {}),
            "capture_utc": capture_utc,
            "analyst_id": self.analyst_id,
            "tool": "osint-posse/evidence_preservation",
            "package_version": package_version,
            "capture_parameters": {
                "max_response_bytes": self.http.max_bytes,
                "timeout_seconds": self.http.timeout,
                "max_redirects": self.http.max_redirects,
            },
            "wayback_submission_requested": submit_to_wayback,
            "requested_artefacts": [
                "screenshot",
                "html",
                "warc",
                *(["wayback"] if submit_to_wayback else []),
            ],
            "python_version": sys.version.split()[0],
            "artefacts": artefacts,
            "proves": [
                "the listed local artefacts matched their SHA-256 values when the receipt was written",
                "the capture tool recorded the listed response metadata",
            ],
            "does_not_prove": [
                "the identity or authority of the operator",
                "continuous custody after acquisition",
                "that the server supplied a complete or authentic representation",
                "that optional capture steps succeeded",
            ],
        }

        log_path = case_dir / "acquisition_receipt.json"
        receipt["receipt_path"] = str(log_path)
        log_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

        return receipt

    @classmethod
    def verify_receipt(cls, receipt_path: str | Path) -> tuple[bool, list[str]]:
        """Verify every captured local artefact hash named by a receipt."""
        path = Path(receipt_path)
        receipt = json.loads(path.read_text(encoding="utf-8"))
        errors: list[str] = []
        if receipt.get("record_type") != "acquisition_receipt":
            errors.append("record_type is not acquisition_receipt")
        for artefact in receipt.get("artefacts", []):
            expected = artefact.get("sha256")
            raw_path = artefact.get("path")
            if not expected or not raw_path:
                continue
            artefact_path = Path(raw_path)
            if not artefact_path.is_file():
                errors.append(f"missing artefact: {artefact_path}")
            elif cls.sha256_file(artefact_path) != expected:
                errors.append(f"hash mismatch: {artefact_path}")
        return not errors, errors

    async def preserve_batch(self, urls: list, submit_to_wayback: bool = True) -> list:
        """Preserve multiple URLs sequentially (respects rate limits)."""
        results = []
        for url in urls:
            result = await self.preserve(url, submit_to_wayback=submit_to_wayback)
            results.append(result)
            await asyncio.sleep(1)  # Rate limit courtesy
        return results


async def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Evidence preservation pipeline")
    parser.add_argument("urls", nargs="+", help="URLs to preserve")
    parser.add_argument("--output", "-o", default="./evidence", help="Output directory")
    parser.add_argument("--analyst", default="green-ink", help="Analyst identifier")
    parser.add_argument("--no-wayback", action="store_true", help="Skip Wayback Machine submission")
    args = parser.parse_args()

    ep = EvidencePreserver(output_dir=args.output, analyst_id=args.analyst)
    failures = 0
    for url in args.urls:
        try:
            result = await ep.preserve(url, submit_to_wayback=not args.no_wayback)
        except Exception as exc:
            failures += 1
            print(f"{url} -- preservation failed: {exc}", file=sys.stderr)
            continue

        expected_status = {
            "screenshot": "captured",
            "html": "captured",
            "warc": "created",
            "wayback": "submitted",
        }
        requested = set(result["requested_artefacts"])
        by_type = {item.get("type"): item for item in result["artefacts"]}
        incomplete = [
            name
            for name in requested
            if by_type.get(name, {}).get("status") != expected_status[name]
        ]
        captured = len(requested) - len(incomplete)
        print(
            f"{result['requested_url']} -- {captured}/{len(requested)} requested artefacts "
            f"preserved -> {result['case_directory']}"
        )
        if incomplete:
            failures += 1
            print(
                "Incomplete preservation: " + ", ".join(sorted(incomplete)),
                file=sys.stderr,
            )
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
