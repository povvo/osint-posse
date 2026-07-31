#!/usr/bin/env python3
"""Dashboard / BI tool.

Builds KPI summaries from case/task/risk CSV files and writes a JSON dashboard
plus a lightweight Markdown view.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict]:
    if not path or not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def count_by(rows: list[dict], field: str) -> dict[str, int]:
    return dict(Counter(str(row.get(field, "blank") or "blank") for row in rows))


def build(tasks: Path | None, risks: Path | None, cases: Path | None, output_dir: Path) -> dict:
    task_rows, risk_rows, case_rows = read_csv(tasks) if tasks else [], read_csv(risks) if risks else [], read_csv(cases) if cases else []
    dashboard = {
        "generated_utc": now(),
        "task_count": len(task_rows),
        "risk_count": len(risk_rows),
        "case_count": len(case_rows),
        "tasks_by_status": count_by(task_rows, "status"),
        "tasks_by_owner": count_by(task_rows, "owner"),
        "risks_by_severity": count_by(risk_rows, "severity"),
        "cases_by_status": count_by(case_rows, "status"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dashboard.json").write_text(json.dumps(dashboard, indent=2), encoding="utf-8")
    lines = ["# Operational Dashboard", "", f"Generated: {dashboard['generated_utc']}", "", f"- Tasks: {len(task_rows)}", f"- Risks: {len(risk_rows)}", f"- Cases: {len(case_rows)}", "", "## Tasks by Status", ""]
    lines += [f"- {k}: {v}" for k, v in dashboard["tasks_by_status"].items()]
    lines += ["", "## Risks by Severity", ""] + [f"- {k}: {v}" for k, v in dashboard["risks_by_severity"].items()]
    (output_dir / "dashboard.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dashboard | {"output_dir": str(output_dir)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create JSON/Markdown KPI dashboard from CSV inputs.")
    ap.add_argument("--tasks"); ap.add_argument("--risks"); ap.add_argument("--cases"); ap.add_argument("--output-dir", default="dashboard")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.tasks) if args.tasks else None, Path(args.risks) if args.risks else None, Path(args.cases) if args.cases else None, Path(args.output_dir)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
