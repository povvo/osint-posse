#!/usr/bin/env python3
"""Specialised Research Templates.

Creates topic-specific research templates from a reusable section library. Useful
for subject, place, organisation, event, and collection-gap research.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

TEMPLATES = {
    "subject": ["Identity", "Timeline", "Associations", "Sources", "Gaps"],
    "organisation": ["Registration", "Control", "Activities", "Links", "Records"],
    "place": ["Boundaries", "History", "Institutions", "Maps", "Local Sources"],
    "event": ["Chronology", "Actors", "Location", "Sources", "Open Questions"],
    "gap": ["Known Unknown", "Why It Matters", "Search Plan", "Owner", "Stop Condition"],
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(kind: str, title: str, output: Path) -> dict:
    if kind not in TEMPLATES:
        raise ValueError(f"kind must be one of {sorted(TEMPLATES)}")
    lines = [f"# {title}", "", f"Template kind: {kind}", f"Created: {now()}", ""]
    for section in TEMPLATES[kind]:
        lines += [f"## {section}", "", "- ", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "kind": kind, "sections": TEMPLATES[kind]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a specialised research template.")
    parser.add_argument("--kind", choices=sorted(TEMPLATES), required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", default="specialised_research_template.md")
    args = parser.parse_args()
    print(json.dumps(create(args.kind, args.title, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
