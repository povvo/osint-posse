#!/usr/bin/env python3
"""Document editor / report template.

Creates a formal report template with source-backed findings, methodology,
limitations, appendices, and review controls.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Executive Summary", "Tasking and Scope", "Methodology", "Source Base", "Findings", "Assessment", "Limitations", "Recommendations", "Appendices", "Review Record"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(title: str, author: str, output: Path) -> dict:
    lines = [f"# {title}", "", f"Author: {author}", f"Created: {now()}", "", "<!-- Keep facts, assumptions, and judgements separated. -->", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "sections": SECTIONS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a structured report template.")
    ap.add_argument("--title", default="Report")
    ap.add_argument("--author", default="analyst")
    ap.add_argument("--output", default="report_template.md")
    args = ap.parse_args()
    print(json.dumps(create(args.title, args.author, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
