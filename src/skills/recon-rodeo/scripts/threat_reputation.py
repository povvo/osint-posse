#!/usr/bin/env python3
"""
ospo :: passive threat reputation
Indicator enrichment through public reputation APIs. Passive lookups only; no scanning or exploitation.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict, field
from typing import Any
from urllib.parse import urlparse

from osint_common import PublicSourceClient, ensure_dir, slugify, utc_now, write_json


@dataclass
class IndicatorReputation:
    indicator: str
    indicator_type: str
    sources: dict[str, Any] = field(default_factory=dict)
    risk_flags: list[str] = field(default_factory=list)
    collected_at_utc: str = field(default_factory=utc_now)


class URLHausClient:
    BASE = "https://urlhaus-api.abuse.ch/v1"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def lookup_url(self, url: str) -> dict[str, Any]:
        # URLhaus expects form data; use urllib for a minimal POST.
        import urllib.parse
        import urllib.request
        data = urllib.parse.urlencode({"url": url}).encode()
        req = urllib.request.Request(f"{self.BASE}/url/", data=data, headers={"User-Agent": self.http.user_agent}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.http.timeout) as resp:  # noqa: S310 - public API endpoint
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    def lookup_host(self, host: str) -> dict[str, Any]:
        import urllib.parse
        import urllib.request
        data = urllib.parse.urlencode({"host": host}).encode()
        req = urllib.request.Request(f"{self.BASE}/host/", data=data, headers={"User-Agent": self.http.user_agent}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.http.timeout) as resp:  # noqa: S310
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}


class OTXClient:
    BASE = "https://otx.alienvault.com/api/v1/indicators"

    def __init__(self, http: PublicSourceClient, api_key: str | None = None):
        self.http = http
        self.api_key = api_key or os.getenv("OTX_API_KEY")

    def lookup(self, indicator: str, indicator_type: str) -> dict[str, Any]:
        if not self.api_key:
            return {"skipped": "OTX_API_KEY not set"}
        otx_type = {"ip": "IPv4", "domain": "domain", "url": "url", "hash": "file"}.get(indicator_type, indicator_type)
        url = f"{self.BASE}/{otx_type}/{indicator}/general"
        return self.http.get_json(url, headers={"X-OTX-API-KEY": self.api_key}, cache_ttl_seconds=3600)  # type: ignore[arg-type]


class ThreatReputation:
    def __init__(self, output_dir: str = "./threat_reputation"):
        self.output_dir = ensure_dir(output_dir)
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", min_interval_seconds=1.0)
        self.urlhaus = URLHausClient(http)
        self.otx = OTXClient(http)

    def classify_indicator(self, indicator: str) -> str:
        if indicator.startswith("http://") or indicator.startswith("https://"):
            return "url"
        if len(indicator) in {32, 40, 64} and all(c in "0123456789abcdefABCDEF" for c in indicator):
            return "hash"
        if all(part.isdigit() and 0 <= int(part) <= 255 for part in indicator.split(".")) and indicator.count(".") == 3:
            return "ip"
        return "domain"

    def enrich(self, indicator: str) -> dict[str, Any]:
        itype = self.classify_indicator(indicator)
        rep = IndicatorReputation(indicator=indicator, indicator_type=itype)
        if itype == "url":
            rep.sources["urlhaus"] = self.urlhaus.lookup_url(indicator)
            host = urlparse(indicator).hostname or ""
            if host:
                rep.sources["urlhaus_host"] = self.urlhaus.lookup_host(host)
        elif itype == "domain":
            rep.sources["urlhaus_host"] = self.urlhaus.lookup_host(indicator)
        rep.sources["otx"] = self.otx.lookup(indicator, itype)
        self._score(rep)
        data = asdict(rep)
        out = self.output_dir / f"reputation_{slugify(indicator)}.json"
        write_json(out, data)
        data["output_path"] = str(out)
        return data

    @staticmethod
    def _score(rep: IndicatorReputation) -> None:
        urlhaus = rep.sources.get("urlhaus") or rep.sources.get("urlhaus_host") or {}
        if isinstance(urlhaus, dict):
            if urlhaus.get("query_status") in {"ok", "malware_download"}:
                rep.risk_flags.append("urlhaus_positive")
            if urlhaus.get("url_status") == "online":
                rep.risk_flags.append("malicious_url_online")
        otx = rep.sources.get("otx", {})
        if isinstance(otx, dict) and otx.get("pulse_info", {}).get("count", 0):
            rep.risk_flags.append("otx_pulses_present")


def main() -> None:
    parser = argparse.ArgumentParser(description="Passive indicator reputation lookup")
    parser.add_argument("indicator")
    parser.add_argument("--out-dir", default="./threat_reputation")
    args = parser.parse_args()
    print(json.dumps(ThreatReputation(args.out_dir).enrich(args.indicator), indent=2))


if __name__ == "__main__":
    main()
