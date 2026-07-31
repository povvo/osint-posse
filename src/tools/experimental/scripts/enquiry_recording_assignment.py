#!/usr/bin/env python3
"""Enquiry Recording and Assignment.

Records enquiries, assigns owners, tracks due dates and status, and exports both
CSV and JSON audit views.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import date, datetime, timezone
from pathlib import Path

FIELDS = ["enquiry_id", "created_utc", "assigned_to", "status", "due", "priority", "question", "source_ref", "result", "closed_utc"]
STATUSES = {"open", "assigned", "blocked", "closed", "cancelled"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rows(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(data)
    path.with_suffix(".json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def add(path: Path, question: str, owner: str, due: str, priority: str, source_ref: str) -> dict:
    if due: date.fromisoformat(due)
    data = rows(path)
    item = {"enquiry_id": str(uuid.uuid4()), "created_utc": now(), "assigned_to": owner, "status": "assigned" if owner else "open", "due": due, "priority": priority, "question": question, "source_ref": source_ref, "result": "", "closed_utc": ""}
    data.append(item); write(path, data); return item


def close(path: Path, enquiry_id: str, result: str) -> dict:
    data = rows(path)
    for item in data:
        if item["enquiry_id"].startswith(enquiry_id):
            item["status"] = "closed"; item["result"] = result; item["closed_utc"] = now(); write(path, data); return item
    raise KeyError(f"enquiry not found: {enquiry_id}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Record and assign enquiries.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("log"); a.add_argument("--question", required=True); a.add_argument("--assigned-to", default=""); a.add_argument("--due", default=""); a.add_argument("--priority", default="normal"); a.add_argument("--source-ref", default="")
    c = sub.add_parser("close"); c.add_argument("log"); c.add_argument("enquiry_id"); c.add_argument("--result", required=True)
    l = sub.add_parser("list"); l.add_argument("log"); l.add_argument("--status")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add(Path(args.log), args.question, args.assigned_to, args.due, args.priority, args.source_ref), indent=2)); return 0
    if args.cmd == "close": print(json.dumps(close(Path(args.log), args.enquiry_id, args.result), indent=2)); return 0
    data = rows(Path(args.log)); print(json.dumps([r for r in data if not args.status or r["status"] == args.status], indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
