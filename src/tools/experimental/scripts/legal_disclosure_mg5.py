#!/usr/bin/env python3
"""Legal Disclosure Preparation (UK MG5 Standard).

Creates a disclosure-preparation checklist and schedule from exhibit/source rows,
including relevance, sensitivity, disclosure status, and reviewer notes.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["item_id", "description", "source_ref", "relevance", "sensitivity", "disclosure_status", "reviewer", "review_note"]
STATUSES = {"pending", "disclose", "withhold_review", "not_relevant"}


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(input_csv: Path, output: Path) -> dict:
    rows = []
    for i, row in enumerate(read(input_csv), 1):
        rows.append({"item_id": row.get("item_id") or row.get("id") or f"item_{i}", "description": row.get("description") or row.get("title") or row.get("note") or "", "source_ref": row.get("source_ref") or row.get("source") or "", "relevance": row.get("relevance", "unknown"), "sensitivity": row.get("sensitivity", "unknown"), "disclosure_status": "pending", "reviewer": "", "review_note": ""})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "items": len(rows), "pending": len(rows)}


def validate(schedule: Path) -> dict:
    rows = read(schedule); findings = []
    for i, row in enumerate(rows, 1):
        if row.get("disclosure_status") not in STATUSES: findings.append({"row": i, "issue": "invalid disclosure_status"})
        if not row.get("reviewer"): findings.append({"row": i, "issue": "reviewer missing"})
    return {"rows": len(rows), "ok": not findings, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build or validate an MG5-style disclosure schedule.")
    ap.add_argument("--input"); ap.add_argument("--output", default="mg5_disclosure_schedule.csv"); ap.add_argument("--validate")
    args = ap.parse_args()
    if args.validate: print(json.dumps(validate(Path(args.validate)), indent=2)); return 0
    if not args.input: ap.error("--input is required unless --validate is used")
    print(json.dumps(build(Path(args.input), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
