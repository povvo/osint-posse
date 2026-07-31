#!/usr/bin/env python3
"""database/task-log.md.

Creates a database-oriented task log schema with CSV, SQLite DDL, and Markdown
field guidance.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = [
    ("task_id", "TEXT PRIMARY KEY", "Stable task identifier"),
    ("case_id", "TEXT", "Case or project identifier"),
    ("created_utc", "TEXT", "Creation timestamp"),
    ("owner", "TEXT", "Responsible person or team"),
    ("status", "TEXT", "open, blocked, waiting, done, cancelled"),
    ("priority", "TEXT", "critical, high, normal, low"),
    ("due", "TEXT", "ISO date"),
    ("task", "TEXT", "Task description"),
    ("result", "TEXT", "Outcome or link to output"),
]


def create(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "database_task_log.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle); writer.writerow([f[0] for f in FIELDS])
    ddl = "CREATE TABLE IF NOT EXISTS task_log (\n" + ",\n".join(f"  {name} {typ}" for name, typ, _ in FIELDS) + "\n);\n"
    ddl_path = output_dir / "task_log_schema.sql"; ddl_path.write_text(ddl, encoding="utf-8")
    md = ["# Database Task Log", "", "| Field | Type | Guidance |", "| --- | --- | --- |"]
    for name, typ, note in FIELDS: md.append(f"| `{name}` | `{typ}` | {note} |")
    md_path = output_dir / "task_log.md"; md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"csv": str(csv_path), "sql": str(ddl_path), "markdown": str(md_path)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create database task log artefacts.")
    ap.add_argument("--output-dir", default="database_task_log")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.output_dir)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
