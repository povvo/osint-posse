#!/usr/bin/env python3
"""BLUF briefing template.

Creates a concise briefing template organised around bottom line, evidence,
confidence, implications, and decision support.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Bottom Line", "Why It Matters", "Evidence Base", "Assessment", "Confidence", "Caveats", "Decision Support", "Next Actions"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(title: str, output: Path) -> dict:
    lines = [f"# {title}", "", f"Created: {now()}", ""]
    for section in SECTIONS:
        prompt = "State this section in concise, source-backed language."
        if section == "Bottom Line": prompt = "One to three sentences. Lead with the answer."
        if section == "Confidence": prompt = "Use standard probability/confidence language."
        lines += [f"## {section}", "", prompt, ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "sections": SECTIONS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a BLUF briefing template.")
    ap.add_argument("--title", default="BLUF Briefing")
    ap.add_argument("--output", default="bluf_briefing.md")
    args = ap.parse_args()
    print(json.dumps(create(args.title, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
