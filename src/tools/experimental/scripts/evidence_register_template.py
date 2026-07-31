#!/usr/bin/env python3
"""templates/database/evidence-register.md.

Creates an evidence-register Markdown template and matching CSV with receipt,
location, hash, custody, review, and disclosure fields.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["evidence_id", "case_id", "description", "received_utc", "received_by", "source_ref", "storage_location", "sha256", "current_holder", "handling", "review_status", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(output_dir: Path, case_id: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "evidence_register.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    md_path = output_dir / "evidence_register.md"
    lines = ["# Evidence Register", "", f"Case ID: {case_id}", f"Created: {now()}", "", "| Field | Guidance |", "| --- | --- |"]
    guidance = {"evidence_id": "Stable evidence identifier", "sha256": "Integrity hash for digital files", "current_holder": "Current custodian", "handling": "Access or handling note", "review_status": "pending/reviewed/excluded"}
    for field in FIELDS: lines.append(f"| `{field}` | {guidance.get(field, 'Evidence metadata')} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"csv": str(csv_path), "markdown": str(md_path), "fields": FIELDS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create evidence-register template files.")
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--output-dir", default="evidence_register_template")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.output_dir), args.case_id), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
