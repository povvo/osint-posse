#!/usr/bin/env python3
"""Task/action log.

Tracks tasks, owners, due dates, status transitions, and unresolved questions in
CSV or JSON form. Designed for small case teams that need auditable handoffs.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import date, datetime, timezone
from pathlib import Path

STATUSES = {"open", "blocked", "waiting", "done", "cancelled"}
FIELDS = ["id", "created_at_utc", "updated_at_utc", "status", "owner", "due", "priority", "summary", "details", "result"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_due(value: str) -> str:
    if not value:
        return ""
    date.fromisoformat(value)
    return value


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    (path.with_suffix(".json")).write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def add_task(path: Path, args: argparse.Namespace) -> dict:
    rows = read_rows(path)
    item = {"id": str(uuid.uuid4()), "created_at_utc": now(), "updated_at_utc": now(), "status": "open", "owner": args.owner or "", "due": validate_due(args.due or ""), "priority": args.priority, "summary": args.summary, "details": args.details or "", "result": ""}
    rows.append(item); write_rows(path, rows); return item


def update_task(path: Path, task_id: str, status: str, result: str = "") -> dict:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {sorted(STATUSES)}")
    rows = read_rows(path)
    for row in rows:
        if row["id"].startswith(task_id):
            row["status"] = status; row["updated_at_utc"] = now()
            if result: row["result"] = result
            write_rows(path, rows); return row
    raise KeyError(f"task not found: {task_id}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Manage a CSV task/action log.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add"); add.add_argument("log"); add.add_argument("--summary", required=True); add.add_argument("--details"); add.add_argument("--owner"); add.add_argument("--due"); add.add_argument("--priority", default="normal")
    upd = sub.add_parser("update"); upd.add_argument("log"); upd.add_argument("task_id"); upd.add_argument("--status", required=True, choices=sorted(STATUSES)); upd.add_argument("--result", default="")
    ls = sub.add_parser("list"); ls.add_argument("log"); ls.add_argument("--status", choices=sorted(STATUSES))
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add_task(Path(args.log), args), indent=2)); return 0
    if args.cmd == "update": print(json.dumps(update_task(Path(args.log), args.task_id, args.status, args.result), indent=2)); return 0
    rows = read_rows(Path(args.log)); rows = [r for r in rows if not args.status or r["status"] == args.status]
    print(json.dumps(rows, indent=2, ensure_ascii=False)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
