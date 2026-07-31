#!/usr/bin/env python3
"""working/findings-memo.md.

Creates a findings memo template with finding, evidence, confidence, caveat, and
recommended action sections.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Purpose", "Key Findings", "Evidence Summary", "Confidence", "Caveats", "Recommended Actions", "Review Record"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(case_id: str, output: Path) -> dict:
    lines = ["# Findings Memo", "", f"Case ID: {case_id}", f"Created: {now()}", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "", ""]
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "sections": SECTIONS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a findings memo template.")
    ap.add_argument("--case-id", required=True); ap.add_argument("--output", default="findings_memo.md")
    args = ap.parse_args()
    print(json.dumps(create(args.case_id, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
