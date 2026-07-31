#!/usr/bin/env python3
"""Master Chronology Construction.

Builds a sorted master chronology from CSV event rows, flags missing dates and
references, and exports Markdown and CSV products.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["date_start", "date_end", "event", "actor", "location", "reference", "confidence", "notes"]


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sort_key(row: dict) -> str:
    return row.get("date_start") or row.get("date") or "9999-99-99"


def build(input_csv: Path, output_csv: Path, output_md: Path) -> dict:
    rows = read(input_csv)
    findings = []
    for idx, row in enumerate(rows, 1):
        if not (row.get("date_start") or row.get("date")):
            findings.append({"row": idx, "issue": "missing date"})
        if not (row.get("reference") or row.get("source_ref") or row.get("source")):
            findings.append({"row": idx, "issue": "missing reference"})
    rows.sort(key=sort_key)
    fields = sorted({k for r in rows for k in r}) if rows else FIELDS
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    lines = ["# Master Chronology", ""]
    for row in rows:
        date = row.get("date_start") or row.get("date") or "undated"
        event = row.get("event") or row.get("description") or row.get("note") or ""
        ref = row.get("reference") or row.get("source_ref") or row.get("source", "")
        lines.append(f"- **{date}** - {event} [{ref}]")
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"events": len(rows), "findings": findings, "csv": str(output_csv), "markdown": str(output_md)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Construct a sorted master chronology.")
    ap.add_argument("events_csv")
    ap.add_argument("--csv-output", default="master_chronology.csv")
    ap.add_argument("--markdown-output", default="master_chronology.md")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.events_csv), Path(args.csv_output), Path(args.markdown_output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
