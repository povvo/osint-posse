#!/usr/bin/env python3
"""templates/database/task-log.md.

Creates a database-ready task log template in Markdown and CSV form with task ID,
owner, status, due date, dependency, and result fields.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["task_id", "created_utc", "owner", "status", "priority", "due", "dependency", "task", "result", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create(output_dir: Path, case_id: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "task_log.csv"
    md_path = output_dir / "task_log.md"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
    lines = ["# Task Log", "", f"Case ID: {case_id}", f"Created: {now()}", "", "| Field | Purpose |", "| --- | --- |"]
    purposes = {"task_id": "Stable identifier", "owner": "Responsible person/team", "status": "open/blocked/waiting/done", "dependency": "Task that must finish first", "result": "Outcome or link to result"}
    for field in FIELDS:
        lines.append(f"| `{field}` | {purposes.get(field, 'Operational task metadata')} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"csv": str(csv_path), "markdown": str(md_path), "fields": FIELDS}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create task log Markdown and CSV templates.")
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--output-dir", default="task_log_template")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.output_dir), args.case_id), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
