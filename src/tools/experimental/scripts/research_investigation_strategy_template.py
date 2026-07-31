#!/usr/bin/env python3
"""Research investigation strategy template.

Creates a strategy document with scope, questions, source plan, risk controls,
review cadence, and stop conditions.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = [
    ("Objective", "What decision or question this work supports."),
    ("Scope", "Included and excluded people, entities, dates, topics, and geographies."),
    ("Key Questions", "Prioritised questions to answer."),
    ("Source Plan", "Source classes to review and why each is relevant."),
    ("Collection Limits", "Legal, ethical, policy, access, time, and data-quality limits."),
    ("Assumptions", "Assumptions that must be tested or monitored."),
    ("Negative Search Plan", "Searches likely to return nothing but worth recording."),
    ("Review Cadence", "When the plan is re-evaluated and by whom."),
    ("Stop Conditions", "Conditions that end or pause the work."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build(title: str, case_id: str, owner: str, output: Path) -> dict:
    lines = [f"# {title}", "", f"Case ID: {case_id}", f"Owner: {owner}", f"Created: {now()}", ""]
    for heading, prompt in SECTIONS:
        lines += [f"## {heading}", "", f"Prompt: {prompt}", "", "- ", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    manifest = {"output": str(output), "title": title, "case_id": case_id, "owner": owner, "sections": [s[0] for s in SECTIONS], "created_at_utc": now()}
    output.with_suffix(".json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a research strategy Markdown template.")
    ap.add_argument("--title", default="Investigation Strategy")
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--owner", default="analyst")
    ap.add_argument("--output", default="investigation_strategy.md")
    args = ap.parse_args()
    print(json.dumps(build(args.title, args.case_id, args.owner, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
