#!/usr/bin/env python3
"""working/briefing.md.

Creates a briefing template with BLUF, facts, assessment, source summary,
confidence language, caveats, and decision asks.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["BLUF", "Context", "Facts", "Assessment", "Source Summary", "Confidence", "Caveats", "Decision Ask", "Next Steps"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(title: str, audience: str, output: Path) -> dict:
    lines = [f"# {title}", "", f"Audience: {audience}", f"Created: {now()}", ""]
    prompts = {"BLUF": "One to three sentences stating the bottom line first.", "Facts": "Only source-backed facts.", "Assessment": "Analytic judgement separated from fact.", "Decision Ask": "What the recipient must decide or do."}
    for section in SECTIONS:
        lines += [f"## {section}", "", prompts.get(section, "Complete this section."), ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "sections": SECTIONS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a briefing Markdown template.")
    ap.add_argument("--title", default="Briefing")
    ap.add_argument("--audience", default="decision maker")
    ap.add_argument("--output", default="briefing.md")
    args = ap.parse_args()
    print(json.dumps(create(args.title, args.audience, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
