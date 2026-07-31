#!/usr/bin/env python3
"""Timestamp normalisation script.

Converts a CSV date/time column to UTC using a declared numeric offset and records
the assumption used for each row.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone, timedelta
from pathlib import Path


def parse_offset(value: str) -> timezone:
    sign = 1 if value[0] == "+" else -1
    hours, minutes = value[1:].split(":", 1)
    return timezone(sign * timedelta(hours=int(hours), minutes=int(minutes)))


def convert(value: str, tz: timezone) -> str:
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(input_csv: Path, output_csv: Path, column: str, offset: str, assumption: str) -> dict:
    tz = parse_offset(offset)
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    for field in ["utc_timestamp", "timestamp_assumption", "timestamp_status"]:
        if field not in fields:
            fields.append(field)
    failed = 0
    for row in rows:
        out = convert(row.get(column, ""), tz)
        row["utc_timestamp"] = out
        row["timestamp_status"] = "ok" if out else "failed"
        row["timestamp_assumption"] = assumption or f"input without timezone treated as {offset}"
        failed += 0 if out else 1
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    return {"output": str(output_csv), "rows": len(rows), "failed": failed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalise a timestamp column to UTC.")
    parser.add_argument("input_csv")
    parser.add_argument("--column", required=True)
    parser.add_argument("--offset", required=True)
    parser.add_argument("--assumption", default="")
    parser.add_argument("--output", default="normalised_timestamps.csv")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.input_csv), Path(args.output), args.column, args.offset, args.assumption), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
