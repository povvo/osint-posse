#!/usr/bin/env python3
"""Timesketch event exporter.

Converts chronology rows into a Timesketch-friendly CSV with datetime,
message, source, tags, and comment fields.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["datetime", "timestamp_desc", "message", "source", "tags", "comment"]


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build(input_csv: Path, output_csv: Path, date_col: str, message_col: str) -> dict:
    rows = read_rows(input_csv)
    out = []
    findings = []
    for idx, row in enumerate(rows, 1):
        dt = row.get(date_col) or row.get("date") or row.get("timestamp") or ""
        msg = row.get(message_col) or row.get("event") or row.get("description") or ""
        if not dt:
            findings.append({"row": idx, "issue": "missing datetime"})
        out.append({"datetime": dt, "timestamp_desc": row.get("time_basis", "observed"), "message": msg, "source": row.get("source_ref") or row.get("source") or "", "tags": row.get("tags", ""), "comment": row.get("notes", "")})
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(out)
    return {"output": str(output_csv), "events": len(out), "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export chronology CSV rows for Timesketch-style import.")
    parser.add_argument("input_csv")
    parser.add_argument("--date-col", default="date_start")
    parser.add_argument("--message-col", default="event")
    parser.add_argument("--output", default="timesketch_events.csv")
    args = parser.parse_args()
    print(json.dumps(build(Path(args.input_csv), Path(args.output), args.date_col, args.message_col), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
