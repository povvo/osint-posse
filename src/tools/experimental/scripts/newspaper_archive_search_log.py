#!/usr/bin/env python3
"""Newspaper archive databases.

Maintains a search log for newspaper archive research, including title, date
range, place, search terms, results, citations, and negative findings.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["search_id", "time_utc", "archive", "newspaper", "place", "date_range", "search_terms", "result_summary", "citation", "negative_finding", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def add(path: Path, args: argparse.Namespace) -> dict:
    rows = read(path)
    row = {"search_id": str(uuid.uuid4()), "time_utc": now(), "archive": args.archive, "newspaper": args.newspaper, "place": args.place, "date_range": args.date_range, "search_terms": args.search_terms, "result_summary": args.result_summary, "citation": args.citation, "negative_finding": args.negative_finding, "notes": args.notes}
    rows.append(row); write(path, rows); return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Record newspaper archive searches and results.")
    parser.add_argument("log"); parser.add_argument("--archive", required=True); parser.add_argument("--newspaper", default=""); parser.add_argument("--place", default=""); parser.add_argument("--date-range", default=""); parser.add_argument("--search-terms", required=True); parser.add_argument("--result-summary", default=""); parser.add_argument("--citation", default=""); parser.add_argument("--negative-finding", default="no"); parser.add_argument("--notes", default=""); parser.add_argument("--list", action="store_true")
    args = parser.parse_args(); path = Path(args.log)
    if args.list:
        print(json.dumps(read(path), indent=2)); return 0
    print(json.dumps(add(path, args), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
