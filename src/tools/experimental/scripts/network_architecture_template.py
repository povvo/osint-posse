#!/usr/bin/env python3
"""analysis/network-architecture.md.

Creates a network architecture worksheet covering nodes, edges, layers, evidence
links, visual rules, and unresolved graph questions.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Network Purpose", "Node Classes", "Edge Classes", "Data Sources", "Layering Rules", "Visual Grammar", "Quality Checks", "Open Questions"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build(case_id: str, output: Path) -> dict:
    lines = ["# Network Architecture", "", f"Case ID: {case_id}", f"Created: {now()}", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "- ", ""]
    lines += ["## Suggested Edge CSV Columns", "", "`source,target,relationship,source_ref,confidence,start_date,end_date,notes`", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    result = {"output": str(output), "case_id": case_id, "sections": SECTIONS}
    output.with_suffix(".json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a network architecture Markdown worksheet.")
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--output", default="network_architecture.md")
    args = ap.parse_args()
    print(json.dumps(build(args.case_id, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
