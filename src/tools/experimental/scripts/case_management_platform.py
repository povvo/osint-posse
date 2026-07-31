#!/usr/bin/env python3
"""Case management platform.

A local case tracker with cases, milestones, tasks, risks, and status summaries in
a single JSON file.
"""
from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

STATUSES = {"new", "active", "paused", "closed"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict:
    if not path.exists(): return {"cases": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def create_case(path: Path, title: str, owner: str, summary: str) -> dict:
    data = load(path)
    case = {"case_id": str(uuid.uuid4()), "title": title, "owner": owner, "summary": summary, "status": "new", "created_at_utc": now(), "updated_at_utc": now(), "tasks": [], "risks": [], "milestones": []}
    data["cases"].append(case); save(path, data); return case


def find_case(data: dict, case_id: str) -> dict:
    for case in data.get("cases", []):
        if case["case_id"].startswith(case_id): return case
    raise KeyError(case_id)


def add_item(path: Path, case_id: str, bucket: str, text: str, owner: str = "") -> dict:
    if bucket not in {"tasks", "risks", "milestones"}: raise ValueError("bucket must be tasks, risks, or milestones")
    data = load(path); case = find_case(data, case_id)
    item = {"id": str(uuid.uuid4()), "text": text, "owner": owner, "status": "open", "created_at_utc": now()}
    case[bucket].append(item); case["updated_at_utc"] = now(); save(path, data); return item


def summary(data: dict) -> dict:
    return {"cases": len(data.get("cases", [])), "by_status": {s: sum(1 for c in data.get("cases", []) if c.get("status") == s) for s in sorted(STATUSES)}, "open_tasks": sum(1 for c in data.get("cases", []) for t in c.get("tasks", []) if t.get("status") != "closed")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain a local JSON case tracker.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create"); c.add_argument("store"); c.add_argument("--title", required=True); c.add_argument("--owner", required=True); c.add_argument("--summary", default="")
    a = sub.add_parser("add"); a.add_argument("store"); a.add_argument("case_id"); a.add_argument("--bucket", required=True); a.add_argument("--text", required=True); a.add_argument("--owner", default="")
    s = sub.add_parser("summary"); s.add_argument("store")
    l = sub.add_parser("list"); l.add_argument("store")
    args = ap.parse_args()
    if args.cmd == "create": print(json.dumps(create_case(Path(args.store), args.title, args.owner, args.summary), indent=2)); return 0
    if args.cmd == "add": print(json.dumps(add_item(Path(args.store), args.case_id, args.bucket, args.text, args.owner), indent=2)); return 0
    data = load(Path(args.store)); print(json.dumps(summary(data) if args.cmd == "summary" else data, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
