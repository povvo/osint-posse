#!/usr/bin/env python3
"""
ospo :: web archive intelligence
Wayback CDX, Memento TimeMap and Common Crawl index lookup for historical public web evidence.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict, field
from typing import Any

from osint_common import PublicSourceClient, ensure_dir, slugify, utc_now, write_json


@dataclass
class ArchiveCapture:
    source: str
    original_url: str
    timestamp: str
    archive_url: str
    status_code: str = ""
    mime_type: str = ""
    digest: str = ""
    length: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


class WaybackCDX:
    BASE = "https://web.archive.org/cdx"

    def __init__(self, http: PublicSourceClient | None = None):
        self.http = http or PublicSourceClient(min_interval_seconds=1.0)

    def search(self, url: str, match_type: str = "prefix", collapse: str = "digest", limit: int = 200) -> list[ArchiveCapture]:
        params = {
            "url": url,
            "output": "json",
            "fl": "timestamp,original,statuscode,mimetype,digest,length",
            "filter": "statuscode:200",
            "matchType": match_type,
            "collapse": collapse,
            "limit": limit,
        }
        data = self.http.get_json(f"{self.BASE}", params=params, cache_ttl_seconds=3600)
        if not isinstance(data, list) or len(data) < 2:
            return []
        headers = data[0]
        captures = []
        for row in data[1:]:
            item = dict(zip(headers, row, strict=False))
            ts = item.get("timestamp", "")
            original = item.get("original", "")
            archive_url = f"https://web.archive.org/web/{ts}/{original}" if ts and original else ""
            captures.append(ArchiveCapture(
                source="wayback_cdx",
                original_url=original,
                timestamp=ts,
                archive_url=archive_url,
                status_code=item.get("statuscode", ""),
                mime_type=item.get("mimetype", ""),
                digest=item.get("digest", ""),
                length=item.get("length", ""),
                raw=item,
            ))
        return captures


class CommonCrawlIndex:
    INDEX_LIST = "https://index.commoncrawl.org/collinfo.json"

    def __init__(self, http: PublicSourceClient | None = None):
        self.http = http or PublicSourceClient(min_interval_seconds=1.0)

    def indexes(self) -> list[dict[str, Any]]:
        data = self.http.get_json(self.INDEX_LIST, cache_ttl_seconds=86400)
        return data if isinstance(data, list) else []

    def search_latest(self, url: str, limit: int = 100) -> dict[str, Any]:
        indexes = self.indexes()
        if not indexes:
            return {"error": "No Common Crawl indexes returned"}
        latest = indexes[0]
        api_url = latest.get("cdx-api")
        if not api_url:
            return {"error": "Latest index did not include cdx-api"}
        params = {"url": url, "output": "json", "limit": limit, "filter": "status:200"}
        text = self.http.get(api_url, params=params, cache_ttl_seconds=86400).get("text", "")
        rows = []
        for line in text.splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return {"index": latest, "url": url, "rows": rows, "total": len(rows)}


class ArchiveIntel:
    def __init__(self, output_dir: str = "./archive_intel"):
        self.output_dir = ensure_dir(output_dir)
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", min_interval_seconds=1.0)
        self.wayback = WaybackCDX(http)
        self.commoncrawl = CommonCrawlIndex(http)

    def investigate_url(self, url: str) -> dict[str, Any]:
        wayback = self.wayback.search(url)
        cc = self.commoncrawl.search_latest(url)
        result = {
            "url": url,
            "collected_at_utc": utc_now(),
            "wayback": [asdict(c) for c in wayback],
            "common_crawl": cc,
            "summary": {
                "wayback_captures": len(wayback),
                "common_crawl_rows": cc.get("total", 0) if isinstance(cc, dict) else 0,
                "first_wayback": min((c.timestamp for c in wayback), default=""),
                "latest_wayback": max((c.timestamp for c in wayback), default=""),
            },
        }
        out = self.output_dir / f"archive_{slugify(url)}.json"
        write_json(out, result)
        result["output_path"] = str(out)
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Wayback and Common Crawl for URL/domain history")
    parser.add_argument("url")
    parser.add_argument("--out-dir", default="./archive_intel")
    args = parser.parse_args()
    print(json.dumps(ArchiveIntel(args.out_dir).investigate_url(args.url), indent=2))


if __name__ == "__main__":
    main()
