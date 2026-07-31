#!/usr/bin/env python3
"""BPMN/swimlane modeller.

Converts a process-step CSV into a Markdown swimlane table and Mermaid flowchart
for workflow review.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

FIELDS = ["step_id", "lane", "activity", "next_step", "control", "notes"]


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def safe_id(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip())
    if not text or text[0].isdigit(): text = "S_" + text
    return text


def build(rows: list[dict], output: Path) -> dict:
    findings = []
    ids = {row.get("step_id", "") for row in rows}
    lines = ["# Process Swimlane", "", "| Step | Lane | Activity | Next | Control | Notes |", "| --- | --- | --- | --- | --- | --- |"]
    flow = ["flowchart TD"]
    for i, row in enumerate(rows, 1):
        step = row.get("step_id") or f"step_{i}"
        lane = row.get("lane", "Unassigned")
        activity = row.get("activity", "")
        next_step = row.get("next_step", "")
        if next_step and next_step not in ids: findings.append({"row": i, "issue": "next_step not present", "next_step": next_step})
        lines.append(f"| {step} | {lane} | {activity} | {next_step} | {row.get('control','')} | {row.get('notes','')} |")
        flow.append(f"  {safe_id(step)}[\"{activity or step}\"]")
        if next_step: flow.append(f"  {safe_id(step)} --> {safe_id(next_step)}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines + ["", "## Mermaid", "", "```mermaid", *flow, "```", ""]), encoding="utf-8")
    return {"output": str(output), "steps": len(rows), "findings": findings}


def init(path: Path) -> dict:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
        writer.writerow({"step_id": "s1", "lane": "Analyst", "activity": "Receive task", "next_step": "s2", "control": "scope check", "notes": ""})
        writer.writerow({"step_id": "s2", "lane": "Reviewer", "activity": "Approve plan", "next_step": "", "control": "approval", "notes": ""})
    return {"created": str(path)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or render a swimlane workflow model.")
    ap.add_argument("--init")
    ap.add_argument("--input")
    ap.add_argument("--output", default="swimlane.md")
    args = ap.parse_args()
    if args.init: print(json.dumps(init(Path(args.init)), indent=2)); return 0
    if not args.input: ap.error("use --init or --input")
    print(json.dumps(build(read(Path(args.input)), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
