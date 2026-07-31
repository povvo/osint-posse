#!/usr/bin/env python3
"""Mandatory Recording of Negative Results.

Records searches, checks, or enquiries that returned no useful result, preserving
query terms, source class, rationale, and follow-up conditions.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["negative_id", "time_utc", "case_id", "source_class", "query_or_action", "expected_result", "actual_result", "reason_kept", "retry_condition", "analyst"]


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
    row = {"negative_id": str(uuid.uuid4()), "time_utc": now(), "case_id": args.case_id, "source_class": args.source_class, "query_or_action": args.query, "expected_result": args.expected, "actual_result": args.actual, "reason_kept": args.reason, "retry_condition": args.retry_condition, "analyst": args.analyst}
    rows.append(row); write(path, rows); return row


def main() -> int:
    ap = argparse.ArgumentParser(description="Record negative searches or checks.")
    ap.add_argument("log"); ap.add_argument("--case-id", required=True); ap.add_argument("--source-class", required=True); ap.add_argument("--query", required=True); ap.add_argument("--expected", default=""); ap.add_argument("--actual", default="no result"); ap.add_argument("--reason", required=True); ap.add_argument("--retry-condition", default=""); ap.add_argument("--analyst", default="analyst"); ap.add_argument("--list", action="store_true")
    args = ap.parse_args(); path = Path(args.log)
    if args.list: print(json.dumps(read(path), indent=2)); return 0
    print(json.dumps(add(path, args), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
