#!/usr/bin/env python3
"""
ospo :: toolkit matrix
Lists current and proposed scripts by workflow stage, output type, dependencies and risk controls.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict

from osint_common import write_json


@dataclass(frozen=True)
class ScriptSpec:
    script: str
    stage: str
    task: str
    input_types: tuple[str, ...]
    output_types: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    risk_controls: tuple[str, ...] = ("passive-public-source", "rate-limit", "provenance")


SCRIPTS = (
    ScriptSpec("osint_common.py", "foundation", "HTTP, provenance, cache, hashing, JSONL logging", ("url", "bytes", "json"), ("json", "provenance")),
    ScriptSpec("case_manager.py", "casework", "case folder, manifest, evidence index, export", ("case title",), ("case directory", "zip")),
    ScriptSpec("source_registry.py", "planning", "source catalogue and auth/cost/terms notes", ("category",), ("source list",)),
    ScriptSpec("search_intel.py", "collection", "Exa/Tavily search and extraction ledgers", ("query", "entity"), ("search hits", "source leads"), ("EXA_API_KEY optional", "TAVILY_API_KEY optional")),
    ScriptSpec("news_monitor.py", "monitoring", "GDELT/RSS media coverage and timelines", ("query",), ("articles", "domain counts", "timeline")),
    ScriptSpec("web_archive_intel.py", "preservation", "Wayback/Common Crawl historical URL captures", ("url", "domain"), ("capture list", "archive URLs")),
    ScriptSpec("document_intel.py", "extraction", "local metadata, text, embedded URLs/emails", ("file", "directory"), ("metadata", "text", "hashes"), ("PyPDF2 optional", "python-docx optional", "Pillow optional", "exiftool optional")),
    ScriptSpec("media_verification.py", "verification", "image/video hashes, keyframes, media stats", ("image", "video"), ("perceptual hashes", "frames", "manifest"), ("Pillow optional", "ffmpeg optional")),
    ScriptSpec("email_intel.py", "pivoting", "email syntax, MX/TXT, Gravatar, search pivots", ("email",), ("email context",), ("dnspython optional",)),
    ScriptSpec("phone_intel.py", "pivoting", "phone normalisation and public search pivots", ("phone",), ("number context",), ("phonenumbers optional",)),
    ScriptSpec("public_records.py", "collection", "Wikidata, Wikipedia, OpenAlex, Crossref, CourtListener", ("entity", "query"), ("records", "knowledge graph leads")),
    ScriptSpec("geospatial_context.py", "geolocation", "OSM/Nominatim nearby context", ("lat,lon",), ("features", "reverse geocode")),
    ScriptSpec("threat_reputation.py", "triage", "URLhaus/OTX passive indicator reputation", ("url", "domain", "ip", "hash"), ("reputation", "risk flags"), ("OTX_API_KEY optional",)),
    ScriptSpec("blockchain_intel.py", "financial", "BTC/ETH public address context", ("crypto address",), ("balance", "transactions"), ("ETHERSCAN_API_KEY optional",)),
    ScriptSpec("visualisation_suite.py", "analysis", "charts, point maps, artefact index", ("json",), ("png", "html"), ("matplotlib optional", "folium optional")),
    ScriptSpec("data_normaliser.py", "analysis", "normalise outputs to POLE entity/edge graph", ("json outputs",), ("normalised graph json",)),
    ScriptSpec("orchestrator.py", "workflow", "safe first-pass bundle by seed type", ("seed",), ("case folder", "module outputs")),
)


def list_scripts(stage: str | None = None) -> list[dict]:
    rows = [asdict(s) for s in SCRIPTS]
    return [r for r in rows if r["stage"] == stage] if stage else rows


def main() -> None:
    parser = argparse.ArgumentParser(description="List custom OSINT scripts by workflow stage")
    parser.add_argument("--stage")
    parser.add_argument("--out")
    args = parser.parse_args()
    rows = list_scripts(args.stage)
    if args.out:
        write_json(args.out, rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
