#!/usr/bin/env python3
"""Identifying Temporal Gaps.

Reads a chronology CSV, sorts events by date, and reports gaps larger than a
configured threshold. It also flags undated events that cannot be sequenced.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import date
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def parse_day(value: str) -> date | None:
    value = (value or "").strip()[:10]
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def analyse(rows: list[dict], date_col: str, threshold_days: int) -> dict:
    dated = []
    undated = []
    for idx, row in enumerate(rows, 1):
        day = parse_day(row.get(date_col, ""))
        if day:
            dated.append((day, idx, row))
        else:
            undated.append({"row": idx, "event": row.get("event") or row.get("description") or ""})
    dated.sort(key=lambda item: item[0])
    gaps = []
    for (left_day, left_idx, left_row), (right_day, right_idx, right_row) in zip(dated, dated[1:]):
        delta = (right_day - left_day).days
        if delta > threshold_days:
            gaps.append({"from_row": left_idx, "to_row": right_idx, "from_date": left_day.isoformat(), "to_date": right_day.isoformat(), "gap_days": delta, "from_event": left_row.get("event", ""), "to_event": right_row.get("event", "")})
    return {"dated_events": len(dated), "undated_events": undated, "gap_threshold_days": threshold_days, "gaps": gaps}


def main() -> int:
    parser = argparse.ArgumentParser(description="Identify large gaps in a chronology CSV.")
    parser.add_argument("chronology_csv")
    parser.add_argument("--date-col", default="date_start")
    parser.add_argument("--threshold-days", type=int, default=30)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = analyse(read_rows(Path(args.chronology_csv)), args.date_col, args.threshold_days)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
