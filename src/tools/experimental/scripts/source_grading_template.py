#!/usr/bin/env python3
"""research/source-grading.md.

Creates a source-grading worksheet and CSV template using separate source
reliability and information credibility fields.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["source_id", "source_name", "claim", "reliability", "credibility", "corroboration", "handling_note", "reviewer", "reviewed_utc"]
RELIABILITY = {"A": "completely reliable", "B": "usually reliable", "C": "fairly reliable", "D": "not usually reliable", "E": "unreliable", "F": "cannot judge"}
CREDIBILITY = {"1": "confirmed", "2": "probably true", "3": "possibly true", "4": "doubtful", "5": "improbable", "6": "cannot judge"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "source_grading.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
    md = ["# Source Grading", "", f"Created: {now()}", "", "## Reliability"]
    md += [f"- {k}: {v}" for k, v in RELIABILITY.items()]
    md += ["", "## Credibility"] + [f"- {k}: {v}" for k, v in CREDIBILITY.items()]
    md += ["", "## Fields", ", ".join(f"`{f}`" for f in FIELDS)]
    md_path = output_dir / "source_grading.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"csv": str(csv_path), "markdown": str(md_path), "fields": FIELDS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create source-grading Markdown and CSV templates.")
    ap.add_argument("--output-dir", default="source_grading_template")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.output_dir)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
