#!/usr/bin/env python3
"""working/report.md.

Creates a working report template that separates draft notes from reviewed
findings and keeps a visible unresolved-issues section.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Draft Summary", "Reviewed Findings", "Evidence Table", "Assumptions", "Unresolved Issues", "Reviewer Notes", "Change Log"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(case_id: str, output: Path) -> dict:
    lines = ["# Working Report", "", f"Case ID: {case_id}", f"Created: {now()}", "", "<!-- Draft material below is not final until reviewed. -->", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "- ", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "sections": SECTIONS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a working report Markdown template.")
    ap.add_argument("--case-id", required=True); ap.add_argument("--output", default="working_report.md")
    args = ap.parse_args()
    print(json.dumps(create(args.case_id, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
