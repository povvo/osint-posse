#!/usr/bin/env python3
"""
ospo :: search intelligence
Unified Exa + Tavily search/extract client with provenance, source deduplication and query ledgers.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict, field
from typing import Any, Optional

from osint_common import JsonlAuditLog, PublicSourceClient, SourceProvenance, ensure_dir, sha256_bytes, slugify, utc_now, write_json


@dataclass
class SearchHit:
    engine: str
    query: str
    title: str
    url: str
    snippet: str = ""
    published_date: str = ""
    score: Optional[float] = None
    raw: dict[str, Any] = field(default_factory=dict)
    collected_at_utc: str = field(default_factory=utc_now)


class ExaClient:
    BASE = "https://api.exa.ai"

    def __init__(self, api_key: str | None = None, http: PublicSourceClient | None = None):
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        self.http = http or PublicSourceClient(min_interval_seconds=1.0)

    def available(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, num_results: int = 10, search_type: str = "auto", max_age_hours: int | None = None) -> list[SearchHit]:
        if not self.api_key:
            return []
        payload: dict[str, Any] = {
            "query": query,
            "type": search_type,
            "numResults": num_results,
            "contents": {"highlights": True, "summary": True},
            "moderation": True,
        }
        if max_age_hours is not None:
            payload["maxAgeHours"] = max_age_hours
        # urllib stdlib POST wrapper kept local to avoid adding a second HTTP abstraction.
        import urllib.request
        req = urllib.request.Request(
            f"{self.BASE}/search",
            data=json.dumps(payload).encode("utf-8"),
            headers={"x-api-key": self.api_key, "Content-Type": "application/json", "User-Agent": self.http.user_agent},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.http.timeout) as resp:  # noqa: S310 - public API endpoint
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # pragma: no cover - network/API dependent
            return [SearchHit(engine="exa", query=query, title="ERROR", url="", snippet=str(exc))]
        hits = []
        for item in data.get("results", []):
            highlights = item.get("highlights") or []
            snippet = "\n".join(str(x) for x in highlights[:3]) or item.get("summary", "") or item.get("text", "")[:500]
            hits.append(SearchHit(
                engine="exa",
                query=query,
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=snippet,
                published_date=item.get("publishedDate", "") or item.get("published_date", ""),
                score=item.get("score"),
                raw=item,
            ))
        return hits

    def get_contents(self, urls: list[str]) -> dict[str, Any]:
        if not self.api_key:
            return {"error": "EXA_API_KEY not set"}
        import urllib.request
        payload = {"ids": urls, "text": True, "highlights": True, "summary": True}
        req = urllib.request.Request(
            f"{self.BASE}/contents",
            data=json.dumps(payload).encode("utf-8"),
            headers={"x-api-key": self.api_key, "Content-Type": "application/json", "User-Agent": self.http.user_agent},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.http.timeout) as resp:  # noqa: S310
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}


class TavilyClient:
    BASE = "https://api.tavily.com"

    def __init__(self, api_key: str | None = None, http: PublicSourceClient | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.http = http or PublicSourceClient(min_interval_seconds=1.0)

    def available(self) -> bool:
        return bool(self.api_key)

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            return {"error": "TAVILY_API_KEY not set"}
        import urllib.request
        payload = {"api_key": self.api_key, **payload}
        req = urllib.request.Request(
            f"{self.BASE}/{endpoint.lstrip('/')}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": self.http.user_agent},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.http.timeout) as resp:  # noqa: S310
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    def search(self, query: str, max_results: int = 10, search_depth: str = "advanced") -> list[SearchHit]:
        data = self._post("search", {"query": query, "max_results": max_results, "search_depth": search_depth, "include_answer": False, "include_raw_content": False})
        if data.get("error"):
            return [SearchHit(engine="tavily", query=query, title="ERROR", url="", snippet=data["error"])]
        hits = []
        for item in data.get("results", []):
            hits.append(SearchHit(
                engine="tavily",
                query=query,
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
                score=item.get("score"),
                raw=item,
            ))
        return hits

    def extract(self, urls: list[str], query: str = "") -> dict[str, Any]:
        return self._post("extract", {"urls": urls, "extract_depth": "advanced", "format": "markdown", "query": query})

    def map(self, url: str, instructions: str = "Find relevant public pages for OSINT source validation") -> dict[str, Any]:
        return self._post("map", {"url": url, "max_depth": 1, "max_breadth": 20, "limit": 50, "instructions": instructions})


class SearchIntelligence:
    def __init__(self, output_dir: str = "./search_runs", audit_log: JsonlAuditLog | None = None):
        self.output_dir = ensure_dir(output_dir)
        self.audit = audit_log or JsonlAuditLog(self.output_dir / "search_audit.jsonl")
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", audit_log=self.audit)
        self.exa = ExaClient(http=http)
        self.tavily = TavilyClient(http=http)

    @staticmethod
    def dedupe(hits: list[SearchHit]) -> list[SearchHit]:
        seen: set[str] = set()
        deduped = []
        for hit in hits:
            key = hit.url.rstrip("/").lower()
            if not key or key in seen:
                continue
            seen.add(key)
            deduped.append(hit)
        return deduped

    def run_queries(self, queries: list[str], engines: tuple[str, ...] = ("exa", "tavily"), per_query: int = 10) -> dict[str, Any]:
        all_hits: list[SearchHit] = []
        for query in queries:
            if "exa" in engines:
                all_hits.extend(self.exa.search(query, num_results=per_query))
            if "tavily" in engines:
                all_hits.extend(self.tavily.search(query, max_results=per_query))
            self.audit.write("query_run", query=query, engines=list(engines), result_count=len(all_hits))
        deduped = self.dedupe(all_hits)
        result = {
            "run_at_utc": utc_now(),
            "queries": queries,
            "engines": list(engines),
            "hits": [asdict(h) for h in deduped],
            "total_hits": len(deduped),
            "availability": {"exa": self.exa.available(), "tavily": self.tavily.available()},
        }
        out = self.output_dir / f"search_{slugify('_'.join(queries), 60)}.json"
        write_json(out, result)
        result["output_path"] = str(out)
        return result

    def source_leads_for_entity(self, entity: str) -> dict[str, Any]:
        queries = [
            f'"{entity}" official filings public record',
            f'"{entity}" sanctions PEP litigation registry',
            f'"{entity}" domain website officers address',
            f'"{entity}" news investigation report archive',
        ]
        return self.run_queries(queries, per_query=8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Exa/Tavily source discovery")
    parser.add_argument("query", nargs="+", help="Query text. Repeat words are joined into one query unless --multi is used.")
    parser.add_argument("--multi", action="store_true", help="Treat each argument as a separate query")
    parser.add_argument("--engines", default="exa,tavily")
    parser.add_argument("--out-dir", default="./search_runs")
    parser.add_argument("--per-query", type=int, default=10)
    args = parser.parse_args()
    queries = args.query if args.multi else [" ".join(args.query)]
    si = SearchIntelligence(args.out_dir)
    print(json.dumps(si.run_queries(queries, tuple(args.engines.split(",")), args.per_query), indent=2))


if __name__ == "__main__":
    main()
