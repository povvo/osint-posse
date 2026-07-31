#!/usr/bin/env python3
"""Interview/focus-group protocol.

Creates a structured research protocol with consent checks, opening script,
question guide, safeguarding notes, and debrief steps.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = [
    "Purpose and Scope",
    "Participant Criteria",
    "Consent Script",
    "Safeguarding and Withdrawal",
    "Opening Questions",
    "Core Topic Questions",
    "Probes and Follow-ups",
    "Debrief",
    "Data Handling Notes",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(topic: str, output: Path) -> dict:
    lines = [f"# Interview / Focus-Group Protocol: {topic}", "", f"Created: {now()}", ""]
    for section in SECTIONS:
        prompt = "Complete before use."
        if section == "Consent Script":
            prompt = "Explain purpose, voluntary participation, recording, data use, withdrawal, and contact route."
        if section == "Safeguarding and Withdrawal":
            prompt = "Define stop conditions, escalation route, and participant support information."
        lines += [f"## {section}", "", prompt, "", "- ", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "topic": topic, "sections": SECTIONS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an interview or focus-group protocol template.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--output", default="interview_protocol.md")
    args = parser.parse_args()
    print(json.dumps(create(args.topic, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
