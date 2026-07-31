#!/usr/bin/env python3
"""
ospo :: public records collector
Passive wrappers for Wikidata, Wikipedia summaries, OpenAlex, Crossref and CourtListener.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict, field
from typing import Any
from urllib.parse import quote

from osint_common import PublicSourceClient, ensure_dir, slugify, utc_now, write_json


@dataclass
class PublicRecordHit:
    source: str
    title: str
    url: str
    identifier: str = ""
    summary: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


class WikidataClient:
    SPARQL = "https://query.wikidata.org/sparql"
    API = "https://www.wikidata.org/w/api.php"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def search_entities(self, query: str, limit: int = 10) -> list[PublicRecordHit]:
        params = {"action": "wbsearchentities", "search": query, "language": "en", "format": "json", "limit": limit}
        data = self.http.get_json(self.API, params=params, cache_ttl_seconds=86400)
        hits = []
        for item in (data or {}).get("search", []) if isinstance(data, dict) else []:
            qid = item.get("id", "")
            hits.append(PublicRecordHit("wikidata", item.get("label", ""), item.get("concepturi", ""), qid, item.get("description", ""), item))
        return hits

    def entity_claims(self, qid: str) -> dict[str, Any]:
        params = {"action": "wbgetentities", "ids": qid, "format": "json", "languages": "en", "props": "labels|descriptions|aliases|claims|sitelinks"}
        data = self.http.get_json(self.API, params=params, cache_ttl_seconds=86400)
        return data if isinstance(data, dict) else {"raw": data}


class WikipediaClient:
    BASE = "https://en.wikipedia.org/api/rest_v1/page/summary"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def summary(self, title: str) -> PublicRecordHit | None:
        data = self.http.get_json(f"{self.BASE}/{quote(title.replace(' ', '_'))}", cache_ttl_seconds=86400)
        if not isinstance(data, dict) or data.get("error"):
            return None
        return PublicRecordHit("wikipedia", data.get("title", title), data.get("content_urls", {}).get("desktop", {}).get("page", ""), data.get("pageid", ""), data.get("extract", ""), data)


class OpenAlexClient:
    BASE = "https://api.openalex.org"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def works(self, query: str, limit: int = 10) -> list[PublicRecordHit]:
        data = self.http.get_json(f"{self.BASE}/works", params={"search": query, "per-page": limit}, cache_ttl_seconds=86400)
        hits = []
        for item in (data or {}).get("results", []) if isinstance(data, dict) else []:
            hits.append(PublicRecordHit("openalex", item.get("title", ""), item.get("id", ""), item.get("doi", "") or item.get("id", ""), item.get("abstract_inverted_index", "") if isinstance(item.get("abstract_inverted_index"), str) else "", item))
        return hits


class CrossrefClient:
    BASE = "https://api.crossref.org/works"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def works(self, query: str, limit: int = 10) -> list[PublicRecordHit]:
        data = self.http.get_json(self.BASE, params={"query": query, "rows": limit}, cache_ttl_seconds=86400)
        hits = []
        items = ((data or {}).get("message", {}).get("items", []) if isinstance(data, dict) else [])
        for item in items:
            title = (item.get("title") or [""])[0]
            hits.append(PublicRecordHit("crossref", title, item.get("URL", ""), item.get("DOI", ""), "", item))
        return hits


class CourtListenerClient:
    BASE = "https://www.courtlistener.com/api/rest/v4/search/"

    def __init__(self, http: PublicSourceClient, token: str | None = None):
        self.http = http
        self.token = token

    def search(self, query: str, limit: int = 10) -> list[PublicRecordHit]:
        headers = {"Authorization": f"Token {self.token}"} if self.token else None
        response = self.http.get(self.BASE, params={"q": query, "page_size": limit}, headers=headers, cache_ttl_seconds=86400)
        try:
            data = json.loads(response.get("text", "{}"))
        except json.JSONDecodeError:
            data = {}
        hits = []
        for item in data.get("results", []):
            hits.append(PublicRecordHit("courtlistener", item.get("caseName", item.get("caseNameFull", "")), item.get("absolute_url", ""), str(item.get("id", "")), item.get("snippet", ""), item))
        return hits


class PublicRecordsCollector:
    def __init__(self, output_dir: str = "./public_records"):
        self.output_dir = ensure_dir(output_dir)
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", min_interval_seconds=1.0)
        self.wikidata = WikidataClient(http)
        self.wikipedia = WikipediaClient(http)
        self.openalex = OpenAlexClient(http)
        self.crossref = CrossrefClient(http)
        self.courtlistener = CourtListenerClient(http)

    def investigate(self, query: str) -> dict[str, Any]:
        hits: list[PublicRecordHit] = []
        hits.extend(self.wikidata.search_entities(query))
        wp = self.wikipedia.summary(query)
        if wp:
            hits.append(wp)
        hits.extend(self.openalex.works(query))
        hits.extend(self.crossref.works(query))
        hits.extend(self.courtlistener.search(query))
        result = {"query": query, "collected_at_utc": utc_now(), "hits": [asdict(h) for h in hits], "total_hits": len(hits)}
        out = self.output_dir / f"public_records_{slugify(query)}.json"
        write_json(out, result)
        result["output_path"] = str(out)
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect public records and knowledge graph leads")
    parser.add_argument("query")
    parser.add_argument("--out-dir", default="./public_records")
    args = parser.parse_args()
    print(json.dumps(PublicRecordsCollector(args.out_dir).investigate(args.query), indent=2))


if __name__ == "__main__":
    main()
