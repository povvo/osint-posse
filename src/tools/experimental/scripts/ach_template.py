#!/usr/bin/env python3
"""analysis/ach.md.

Creates an Analysis of Competing Hypotheses matrix template in CSV and Markdown,
with hypotheses, evidence, diagnosticity, consistency, and notes.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["evidence_id", "evidence", "source_ref", "diagnosticity", "hypothesis", "consistency", "weight", "notes"]


def create(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "ach_matrix.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    md_path = output_dir / "ach.md"
    md_path.write_text("# Analysis of Competing Hypotheses\n\nUse the CSV matrix to score whether each evidence item is consistent, inconsistent, or neutral for each hypothesis.\n", encoding="utf-8")
    return {"csv": str(csv_path), "markdown": str(md_path), "fields": FIELDS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an ACH matrix template.")
    parser.add_argument("--output-dir", default="ach_template")
    args = parser.parse_args()
    print(json.dumps(create(Path(args.output_dir)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
