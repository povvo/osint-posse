#!/usr/bin/env python3
"""Shared, passive OSINT utilities with bounded public-network access."""

from __future__ import annotations

import csv
import hashlib
import http.client
import ipaddress
import json
import os
import random
import re
import socket
import ssl
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional


DEFAULT_USER_AGENT = os.getenv(
    "OSINT_USER_AGENT",
    "green-ink/0.1 (+https://github.com/povvo/ospo; passive-public-source)",
)
DEFAULT_MAX_BYTES = 10 * 1024 * 1024
DEFAULT_MAX_REDIRECTS = 5
SENSITIVE_QUERY_NAME = re.compile(
    r"(?:^|[_-])(?:api[_-]?key|key|token|secret|signature|password|passwd|auth|credential)(?:$|[_-])",
    re.I,
)
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class UnsafeTargetError(ValueError):
    """Raised before a request when a URL can reach a non-public target."""


class FetchLimitError(RuntimeError):
    """Raised when a response exceeds its declared or observed byte budget."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_dir(path: str | Path) -> Path:
    result = Path(path)
    result.mkdir(parents=True, exist_ok=True)
    return result


def slugify(value: str, limit: int = 80) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return (value.strip("._-") or "item")[:limit]


def redact_secret(value: str) -> str:
    if not value:
        return value
    if len(value) <= 8:
        return "***"
    return value[:4] + "…" + value[-4:]


def redact_url(url: str) -> str:
    """Remove credentials, fragments, and recognised query secrets from a URL."""
    parts = urllib.parse.urlsplit(url)
    host = parts.hostname or ""
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    if parts.port:
        host = f"{host}:{parts.port}"
    query = []
    for name, value in urllib.parse.parse_qsl(parts.query, keep_blank_values=True):
        query.append((name, "[REDACTED]" if SENSITIVE_QUERY_NAME.search(name) else value))
    return urllib.parse.urlunsplit((parts.scheme, host, parts.path, urllib.parse.urlencode(query, doseq=True), ""))


def _public_ip(value: str) -> bool:
    address = ipaddress.ip_address(value.split("%", 1)[0])
    return bool(address.is_global)


def validate_public_url(
    url: str,
    resolver: Callable[..., list[tuple[Any, ...]]] = socket.getaddrinfo,
) -> tuple[urllib.parse.SplitResult, tuple[str, ...]]:
    """Resolve and approve only public HTTP(S) addresses."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme.lower() not in {"http", "https"}:
        raise UnsafeTargetError("Only http and https public-source URLs are allowed.")
    if parts.username is not None or parts.password is not None:
        raise UnsafeTargetError("Credentials embedded in URLs are forbidden.")
    host = parts.hostname
    if not host:
        raise UnsafeTargetError("URL hostname is missing.")
    if host.lower() == "localhost" or host.lower().endswith(".localhost"):
        raise UnsafeTargetError("Localhost targets are forbidden.")
    port = parts.port or (443 if parts.scheme.lower() == "https" else 80)
    try:
        rows = resolver(host, port, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise UnsafeTargetError(f"Hostname resolution failed for {host!r}.") from exc
    addresses = tuple(dict.fromkeys(row[4][0] for row in rows))
    if not addresses:
        raise UnsafeTargetError(f"Hostname {host!r} resolved to no addresses.")
    if any(not _public_ip(address) for address in addresses):
        raise UnsafeTargetError(f"Hostname {host!r} resolves to a non-public address.")
    return parts, addresses


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host: str, port: int, pinned_ip: str, timeout: float):
        self._pinned_ip = pinned_ip
        super().__init__(host, port, timeout=timeout)

    def connect(self) -> None:
        self.sock = socket.create_connection((self._pinned_ip, self.port), self.timeout)


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, port: int, pinned_ip: str, timeout: float):
        self._pinned_ip = pinned_ip
        super().__init__(host, port, timeout=timeout, context=ssl.create_default_context())

    def connect(self) -> None:
        plain = socket.create_connection((self._pinned_ip, self.port), self.timeout)
        self.sock = self._context.wrap_socket(plain, server_hostname=self.host)


def _read_limited(response: Any, max_bytes: int) -> bytes:
    length = response.getheader("content-length")
    if length:
        try:
            if int(length) > max_bytes:
                raise FetchLimitError(f"Response declares more than {max_bytes} bytes.")
        except ValueError:
            pass
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65536, max_bytes - total + 1))
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise FetchLimitError(f"Response exceeded the {max_bytes}-byte limit.")
        chunks.append(chunk)
    return b"".join(chunks)


def _safe_headers(rows: Iterable[tuple[str, str]]) -> dict[str, str]:
    blocked = {"set-cookie", "proxy-authenticate", "www-authenticate", "authorization"}
    return {name: value for name, value in rows if name.lower() not in blocked}


def _request_once(
    url: str,
    headers: dict[str, str],
    *,
    timeout: float,
    max_bytes: int,
) -> tuple[int, dict[str, str], bytes]:
    parts, addresses = validate_public_url(url)
    port = parts.port or (443 if parts.scheme == "https" else 80)
    connection_type = _PinnedHTTPSConnection if parts.scheme == "https" else _PinnedHTTPConnection
    connection = connection_type(parts.hostname or "", port, addresses[0], timeout)
    target = urllib.parse.urlunsplit(("", "", parts.path or "/", parts.query, ""))
    try:
        connection.request("GET", target, headers=headers)
        response = connection.getresponse()
        body = _read_limited(response, max_bytes)
        return response.status, _safe_headers(response.getheaders()), body
    finally:
        connection.close()


def fetch_public_url(
    url: str,
    headers: dict[str, str],
    *,
    timeout: float,
    max_bytes: int,
    max_redirects: int,
) -> tuple[str, int, dict[str, str], bytes]:
    """Fetch a public URL while pinning each DNS result and checking every redirect."""
    current = url
    seen: set[str] = set()
    deadline = time.monotonic() + timeout
    for redirect_count in range(max_redirects + 1):
        safe_current = redact_url(current)
        if safe_current in seen:
            raise UnsafeTargetError("Redirect loop detected.")
        seen.add(safe_current)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Public-source request exceeded its time limit.")
        status, response_headers, body = _request_once(
            current,
            headers,
            timeout=remaining,
            max_bytes=max_bytes,
        )
        location = next((value for name, value in response_headers.items() if name.lower() == "location"), None)
        if status not in REDIRECT_STATUSES:
            return current, status, response_headers, body
        if not location:
            raise UnsafeTargetError("Redirect response omitted its destination.")
        if redirect_count >= max_redirects:
            raise UnsafeTargetError("Redirect limit exceeded.")
        current = urllib.parse.urljoin(current, location)
        validate_public_url(current)
    raise UnsafeTargetError("Redirect limit exceeded.")


@dataclass
class SourceProvenance:
    source: str
    url: str = ""
    collected_at_utc: str = field(default_factory=utc_now)
    method: str = "GET"
    status_code: Optional[int] = None
    content_type: str = ""
    bytes: int = 0
    sha256: str = ""
    licence: str = "unknown"
    access: str = "public"
    notes: str = ""


@dataclass
class EvidenceItem:
    item_id: str
    item_type: str
    title: str
    value: Any
    confidence: float = 1.0
    source: SourceProvenance = field(default_factory=lambda: SourceProvenance(source="unknown"))
    tags: list[str] = field(default_factory=list)
    related_entities: list[str] = field(default_factory=list)
    analyst_notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class JsonlAuditLog:
    """Append-only JSONL event log for case actions and source access."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        ensure_dir(self.path.parent)

    def write(self, event_type: str, **payload: Any) -> dict[str, Any]:
        event = {"timestamp_utc": utc_now(), "event_type": event_type, **payload}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]


class SimpleCache:
    """Disk cache keyed by a secret-redacted request identity."""

    def __init__(self, cache_dir: str | Path = ".osint_cache"):
        self.cache_dir = ensure_dir(cache_dir)

    def key(self, method: str, url: str, body: bytes | None = None) -> str:
        material = method.upper().encode() + b"\0" + redact_url(url).encode() + b"\0" + (body or b"")
        return sha256_bytes(material)

    def path_for(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str, max_age_seconds: int | None = None) -> Optional[dict[str, Any]]:
        path = self.path_for(key)
        if not path.exists():
            return None
        if max_age_seconds is not None and time.time() - path.stat().st_mtime > max_age_seconds:
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def set(self, key: str, value: dict[str, Any]) -> None:
        self.path_for(key).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class RateLimiter:
    def __init__(self, min_interval_seconds: float = 1.0, jitter_seconds: float = 0.25):
        self.min_interval_seconds = min_interval_seconds
        self.jitter_seconds = jitter_seconds
        self._last_call = 0.0

    def wait(self) -> None:
        delay = self.min_interval_seconds - (time.time() - self._last_call)
        if delay > 0:
            time.sleep(delay + random.uniform(0, self.jitter_seconds))
        self._last_call = time.time()


class PublicSourceClient:
    """HTTP client with DNS pinning, bounded redirects/bytes/time, caching, and provenance."""

    def __init__(
        self,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: int = 30,
        min_interval_seconds: float = 1.0,
        cache_dir: str | Path | None = None,
        audit_log: JsonlAuditLog | None = None,
        max_bytes: int = DEFAULT_MAX_BYTES,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
    ):
        self.user_agent = user_agent
        self.timeout = timeout
        self.rate_limiter = RateLimiter(min_interval_seconds=min_interval_seconds)
        self.cache = SimpleCache(cache_dir) if cache_dir else None
        self.audit_log = audit_log
        self.max_bytes = max_bytes
        self.max_redirects = max_redirects

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {"User-Agent": self.user_agent, "Accept": "application/json, text/plain, */*"}
        if extra:
            headers.update(extra)
        return headers

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        cache_ttl_seconds: int | None = None,
        retries: int = 2,
    ) -> dict[str, Any]:
        if params:
            url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        safe_url = redact_url(url)
        cache_key = self.cache.key("GET", safe_url) if self.cache else ""
        if self.cache:
            cached = self.cache.get(cache_key, cache_ttl_seconds)
            if cached is not None:
                cached["from_cache"] = True
                return cached

        last_error = ""
        for attempt in range(retries + 1):
            self.rate_limiter.wait()
            try:
                final_url, status, response_headers, content = fetch_public_url(
                    url,
                    self._headers(headers),
                    timeout=float(self.timeout),
                    max_bytes=self.max_bytes,
                    max_redirects=self.max_redirects,
                )
                result = {
                    "url": redact_url(final_url),
                    "status_code": status,
                    "headers": response_headers,
                    "text": content.decode("utf-8", errors="replace"),
                    "content_sha256": sha256_bytes(content),
                    "bytes": len(content),
                    "from_cache": False,
                }
                if self.cache:
                    self.cache.set(cache_key, result)
                if self.audit_log:
                    self.audit_log.write("http_get", url=result["url"], status_code=status, bytes=len(content))
                return result
            except (UnsafeTargetError, FetchLimitError) as exc:
                last_error = str(exc)
                break
            except Exception as exc:  # pragma: no cover - network dependent
                last_error = str(exc).replace(url, safe_url)
                if attempt < retries:
                    time.sleep(2**attempt)
        if self.audit_log:
            self.audit_log.write("http_get_failed", url=safe_url, error=last_error)
        return {"url": safe_url, "error": last_error, "status_code": None, "text": "", "headers": {}, "bytes": 0}

    def get_json(self, url: str, **kwargs: Any) -> dict[str, Any] | list[Any]:
        response = self.get(url, **kwargs)
        if response.get("error"):
            return {"error": response["error"], "url": response.get("url")}
        try:
            return json.loads(response.get("text", ""))
        except json.JSONDecodeError:
            return {"error": "response was not valid JSON", "url": response.get("url"), "status_code": response.get("status_code")}

    def provenance(self, source: str, response: dict[str, Any], licence: str = "unknown", notes: str = "") -> SourceProvenance:
        headers = response.get("headers", {}) or {}
        return SourceProvenance(
            source=source,
            url=response.get("url", ""),
            status_code=response.get("status_code"),
            content_type=headers.get("content-type", headers.get("Content-Type", "")),
            bytes=int(response.get("bytes") or 0),
            sha256=response.get("content_sha256", ""),
            licence=licence,
            notes=notes,
        )


def write_json(path: str | Path, data: Any) -> Path:
    result = Path(path)
    ensure_dir(result.parent)
    result.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return result


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_csv(path: str | Path, rows: Iterable[dict[str, Any]]) -> Path:
    result = Path(path)
    ensure_dir(result.parent)
    rows = list(rows)
    fieldnames = sorted({key for row in rows for key in row}) if rows else []
    with result.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return result


def flatten_dict(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            output.update(flatten_dict(value, full_key))
        else:
            output[full_key] = value
    return output
