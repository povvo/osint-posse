#!/usr/bin/env python3
"""
ospo :: news and narrative monitor
GDELT DOC 2.0 + RSS monitoring with coverage volume, tone, domains and article ledgers.
"""

from __future__ import annotations

import argparse
import json
import re
try:
    import defusedxml.ElementTree as ET  # type: ignore[import-untyped]
except ImportError:
    import xml.etree.ElementTree as ET  # type: ignore[no-redef]  # noqa: S405
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode

from osint_common import PublicSourceClient, ensure_dir, slugify, utc_now, write_json


@dataclass
class Article:
    title: str
    url: str
    source: str = ""
    domain: str = ""
    seen_at: str = ""
    language: str = ""
    country: str = ""
    tone: float | None = None
    snippet: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


class GDELTDocClient:
    BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

    def __init__(self, http: PublicSourceClient | None = None):
        self.http = http or PublicSourceClient(min_interval_seconds=1.0)

    def article_search(self, query: str, timespan: str = "1week", max_records: int = 75, sort: str = "hybridrel") -> list[Article]:
        params = {
            "query": query,
            "mode": "ArtList",
            "format": "json",
            "timespan": timespan,
            "maxrecords": max_records,
            "sort": sort,
        }
        data = self.http.get_json(self.BASE, params=params, cache_ttl_seconds=900)
        if isinstance(data, dict) and data.get("error"):
            return []
        articles = []
        for item in (data or {}).get("articles", []):
            articles.append(Article(
                title=item.get("title", ""),
                url=item.get("url", ""),
                source="gdelt_doc",
                domain=item.get("domain", ""),
                seen_at=item.get("seendate", ""),
                language=item.get("language", ""),
                country=item.get("sourcecountry", ""),
                raw=item,
            ))
        return articles

    def timeline(self, query: str, timespan: str = "1month", mode: str = "timelinevolraw") -> dict[str, Any]:
        params = {"query": query, "mode": mode, "format": "json", "timespan": timespan}
        data = self.http.get_json(self.BASE, params=params, cache_ttl_seconds=1800)
        return data if isinstance(data, dict) else {"timeline": data}


class RSSMonitor:
    def __init__(self, http: PublicSourceClient | None = None):
        self.http = http or PublicSourceClient(min_interval_seconds=1.0)

    def fetch_feed(self, feed_url: str, query_filter: str | None = None) -> list[Article]:
        response = self.http.get(feed_url, cache_ttl_seconds=600)
        if response.get("error"):
            return []
        try:
            root = ET.fromstring(response.get("text", ""))
        except ET.ParseError:
            return []
        query_re = re.compile(re.escape(query_filter), re.I) if query_filter else None
        articles = []
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            if query_re and not (query_re.search(title) or query_re.search(desc)):
                continue
            articles.append(Article(title=title, url=link, source="rss", snippet=desc, seen_at=item.findtext("pubDate") or ""))
        return articles


class NarrativeMonitor:
    def __init__(self, output_dir: str = "./news_monitor"):
        self.output_dir = ensure_dir(output_dir)
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", min_interval_seconds=1.0)
        self.gdelt = GDELTDocClient(http)
        self.rss = RSSMonitor(http)

    def collect(self, query: str, rss_feeds: list[str] | None = None, timespan: str = "1week") -> dict[str, Any]:
        articles = self.gdelt.article_search(query, timespan=timespan)
        for feed in rss_feeds or []:
            articles.extend(self.rss.fetch_feed(feed, query_filter=query.strip('"')))
        domains = Counter(a.domain or self._domain(a.url) for a in articles if a.url)
        languages = Counter(a.language for a in articles if a.language)
        countries = Counter(a.country for a in articles if a.country)
        timeline = self.gdelt.timeline(query, timespan=timespan)
        result = {
            "query": query,
            "collected_at_utc": utc_now(),
            "timespan": timespan,
            "articles": [asdict(a) for a in articles],
            "summary": {
                "total_articles": len(articles),
                "top_domains": domains.most_common(20),
                "languages": languages.most_common(20),
                "source_countries": countries.most_common(20),
            },
            "timeline": timeline,
        }
        out = self.output_dir / f"narrative_{slugify(query)}.json"
        write_json(out, result)
        result["output_path"] = str(out)
        return result

    @staticmethod
    def _domain(url: str) -> str:
        m = re.match(r"https?://([^/]+)", url)
        return m.group(1).lower() if m else ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor news and narratives through GDELT/RSS")
    parser.add_argument("query")
    parser.add_argument("--timespan", default="1week")
    parser.add_argument("--rss", action="append", default=[])
    parser.add_argument("--out-dir", default="./news_monitor")
    args = parser.parse_args()
    nm = NarrativeMonitor(args.out_dir)
    print(json.dumps(nm.collect(args.query, args.rss, args.timespan), indent=2))


if __name__ == "__main__":
    main()
