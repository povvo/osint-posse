#!/usr/bin/env python3
"""research/case-decision-log.md.

Creates a case decision log template with structured fields for decision, basis,
alternatives considered, source references, and review date.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["decision_id", "time_utc", "decision", "basis", "alternatives_considered", "source_refs", "owner", "review_date", "status"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(output_dir: Path, case_id: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "case_decision_log.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    md = ["# Case Decision Log", "", f"Case ID: {case_id}", f"Created: {now()}", "", "| Field | Guidance |", "| --- | --- |"]
    guidance = {"decision": "What was decided", "basis": "Why the decision was taken", "alternatives_considered": "Options considered and rejected", "source_refs": "Records supporting the decision", "review_date": "When to revisit"}
    for field in FIELDS: md.append(f"| `{field}` | {guidance.get(field, 'Decision metadata')} |")
    md_path = output_dir / "case_decision_log.md"; md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"csv": str(csv_path), "markdown": str(md_path), "fields": FIELDS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a case decision log template.")
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--output-dir", default="case_decision_log")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.output_dir), args.case_id), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
