#!/usr/bin/env python3
"""Research log template.

Creates a genealogy research log with repository, search terms, record class,
results, citations, negative findings, and next actions.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["log_id", "time_utc", "repository", "record_class", "person_or_family", "search_terms", "date_range", "place", "result", "citation", "negative_finding", "next_action"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(output: Path) -> dict:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
    return {"output": str(output), "fields": FIELDS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a genealogy research log template.")
    parser.add_argument("--output", default="genealogy_research_log.csv")
    args = parser.parse_args()
    print(json.dumps(create(Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
