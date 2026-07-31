#!/usr/bin/env python3
"""Jira / ServiceNow / Linear-style workflow board.

Builds a local kanban board from CSV tasks and exports Markdown plus JSON grouped
by workflow state.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

DEFAULT_STATES = ["backlog", "ready", "in_progress", "blocked", "review", "done"]


def read_tasks(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def group(tasks: list[dict], state_col: str) -> dict[str, list[dict]]:
    board = {state: [] for state in DEFAULT_STATES}
    board["other"] = []
    for task in tasks:
        state = str(task.get(state_col, "backlog")).strip().lower().replace(" ", "_") or "backlog"
        board.setdefault(state, []).append(task)
    return board


def write_markdown(path: Path, board: dict[str, list[dict]], title_col: str) -> None:
    lines = ["# Workflow Board", ""]
    for state, items in board.items():
        if not items: continue
        lines += [f"## {state.replace('_',' ').title()}", ""]
        for item in items:
            title = item.get(title_col) or item.get("summary") or item.get("task") or str(item)
            owner = item.get("owner") or item.get("assignee") or ""
            due = item.get("due") or ""
            lines.append(f"- {title}" + (f" · {owner}" if owner else "") + (f" · due {due}" if due else ""))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def export(input_csv: Path, output_dir: Path, state_col: str, title_col: str) -> dict:
    tasks = read_tasks(input_csv); board = group(tasks, state_col)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "workflow_board.json").write_text(json.dumps(board, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(output_dir / "workflow_board.md", board, title_col)
    return {"tasks": len(tasks), "states": {k: len(v) for k, v in board.items()}, "output_dir": str(output_dir)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a local workflow board from task CSV.")
    ap.add_argument("task_csv"); ap.add_argument("--state-col", default="status"); ap.add_argument("--title-col", default="summary"); ap.add_argument("--output-dir", default="workflow_board")
    args = ap.parse_args()
    print(json.dumps(export(Path(args.task_csv), Path(args.output_dir), args.state_col, args.title_col), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
