#!/usr/bin/env python3
"""NIM assessment template.

Creates a strategic reporting template with intelligence picture, priorities,
risks, gaps, and recommended tasking sections.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Strategic Context", "Tactical Picture", "Priority Threats/Risks", "Current Intelligence", "Intelligence Gaps", "Recommended Tasking", "Review Cycle"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(case_id: str, output: Path) -> dict:
    lines = ["# NIM Assessment", "", f"Case ID: {case_id}", f"Created: {now()}", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "- ", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "sections": SECTIONS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a NIM assessment template.")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--output", default="nim_assessment_template.md")
    args = parser.parse_args()
    print(json.dumps(create(args.case_id, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
