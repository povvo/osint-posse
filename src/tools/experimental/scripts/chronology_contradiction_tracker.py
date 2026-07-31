#!/usr/bin/env python3
"""Chronology contradiction tracker.

Finds conflicting dates, duplicate event identifiers, and source-date mismatches
inside a chronology CSV. Outputs a reviewer-focused JSON report.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def analyse(rows: list[dict], event_col: str, date_col: str, source_date_col: str | None) -> dict:
    by_event: dict[str, list[tuple[int, dict]]] = defaultdict(list)
    findings = []
    for idx, row in enumerate(rows, 1):
        key = str(row.get(event_col, "")).strip() or f"row_{idx}"
        by_event[key].append((idx, row))
        if source_date_col and row.get(date_col) and row.get(source_date_col) and row[date_col] != row[source_date_col]:
            findings.append({"row": idx, "issue": "event date differs from source date", "event_date": row[date_col], "source_date": row[source_date_col]})
    for key, items in by_event.items():
        dates = sorted({str(row.get(date_col, "")).strip() for _, row in items if row.get(date_col)})
        if len(items) > 1 and len(dates) > 1:
            findings.append({"event": key, "issue": "same event has multiple dates", "rows": [idx for idx, _ in items], "dates": dates})
    return {"rows": len(rows), "finding_count": len(findings), "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Track chronology contradictions in CSV rows.")
    parser.add_argument("chronology_csv")
    parser.add_argument("--event-col", default="event_id")
    parser.add_argument("--date-col", default="date_start")
    parser.add_argument("--source-date-col")
    parser.add_argument("--output", default="chronology_contradictions.json")
    args = parser.parse_args()
    result = analyse(read_rows(Path(args.chronology_csv)), args.event_col, args.date_col, args.source_date_col)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "finding_count": result["finding_count"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
