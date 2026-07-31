#!/usr/bin/env python3
"""analysis/chronological-matrix.md.

Creates a chronology matrix template with event, time, source, confidence,
conflict, and gap fields.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["event_id", "date_start", "date_end", "time_basis", "event", "actor", "location", "source_ref", "confidence", "conflict_note", "gap_note"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(output_dir: Path, case_id: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "chronological_matrix.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    md_path = output_dir / "chronological_matrix.md"
    lines = ["# Chronological Matrix", "", f"Case ID: {case_id}", f"Created: {now()}", "", "| Field | Guidance |", "| --- | --- |"]
    for field in FIELDS: lines.append(f"| `{field}` | Chronology metadata |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"csv": str(csv_path), "markdown": str(md_path), "fields": FIELDS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a chronological matrix template.")
    ap.add_argument("--case-id", required=True); ap.add_argument("--output-dir", default="chronological_matrix")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.output_dir), args.case_id), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
