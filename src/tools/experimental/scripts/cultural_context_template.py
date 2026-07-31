#!/usr/bin/env python3
"""research/cultural-context.md.

Creates a cultural-context research template covering language, institutions,
customs, media environment, historical context, and source cautions.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Scope", "Languages and Terms", "Institutions", "Customs and Norms", "Media Environment", "Historical Context", "Source Cautions", "Research Gaps"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(topic: str, output: Path) -> dict:
    lines = [f"# Cultural Context: {topic}", "", f"Created: {now()}", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "- ", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "topic": topic, "sections": SECTIONS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a cultural-context research template.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--output", default="cultural_context.md")
    args = parser.parse_args()
    print(json.dumps(create(args.topic, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
