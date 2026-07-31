#!/usr/bin/env python3
"""Temporal Conflict Resolution.

Compares chronology rows that share an event or entity key and flags conflicting
dates, uncertain source priority, and proposed resolution notes.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def key_for(row: dict, key_col: str) -> str:
    return (row.get(key_col) or row.get("event") or row.get("description") or "").strip().lower()


def analyse(rows: list[dict], key_col: str, date_col: str) -> dict:
    groups: dict[str, list[tuple[int, dict]]] = defaultdict(list)
    for idx, row in enumerate(rows, 1):
        key = key_for(row, key_col)
        if key:
            groups[key].append((idx, row))
    conflicts = []
    for key, items in groups.items():
        dates = {str(row.get(date_col, "")).strip() for _, row in items if str(row.get(date_col, "")).strip()}
        if len(dates) > 1:
            conflicts.append({"key": key, "dates": sorted(dates), "rows": [idx for idx, _ in items], "resolution": "review source reliability, precision, timezone, and original wording"})
    return {"groups": len(groups), "conflicts": conflicts, "conflict_count": len(conflicts)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Find conflicting dates in a chronology CSV.")
    parser.add_argument("chronology_csv")
    parser.add_argument("--key-col", default="event_id")
    parser.add_argument("--date-col", default="date_start")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = analyse(read_rows(Path(args.chronology_csv)), args.key_col, args.date_col)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
