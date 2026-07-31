#!/usr/bin/env python3
"""Physical evidence inventory system.

Tracks physical evidence containers, seals, storage locations, custody holder, and
inspection status in a local CSV ledger.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["item_id", "case_id", "description", "container", "seal", "location", "holder", "status", "updated_utc", "notes"]
STATUSES = {"stored", "checked_out", "released", "disposed", "missing"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def add(path: Path, case_id: str, description: str, container: str, seal: str, location: str, holder: str, notes: str) -> dict:
    rows = read(path)
    row = {"item_id": str(uuid.uuid4()), "case_id": case_id, "description": description, "container": container, "seal": seal, "location": location, "holder": holder, "status": "stored", "updated_utc": now(), "notes": notes}
    rows.append(row); write(path, rows); return row


def update(path: Path, item_id: str, location: str | None, holder: str | None, status: str | None, notes: str | None) -> dict:
    rows = read(path)
    if status and status not in STATUSES: raise ValueError(f"status must be one of {sorted(STATUSES)}")
    for row in rows:
        if row["item_id"].startswith(item_id):
            if location is not None: row["location"] = location
            if holder is not None: row["holder"] = holder
            if status is not None: row["status"] = status
            if notes is not None: row["notes"] = notes
            row["updated_utc"] = now(); write(path, rows); return row
    raise KeyError(item_id)


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain a physical evidence inventory CSV.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("inventory"); a.add_argument("--case-id", required=True); a.add_argument("--description", required=True); a.add_argument("--container", default=""); a.add_argument("--seal", default=""); a.add_argument("--location", default=""); a.add_argument("--holder", default=""); a.add_argument("--notes", default="")
    u = sub.add_parser("update"); u.add_argument("inventory"); u.add_argument("item_id"); u.add_argument("--location"); u.add_argument("--holder"); u.add_argument("--status", choices=sorted(STATUSES)); u.add_argument("--notes")
    l = sub.add_parser("list"); l.add_argument("inventory")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add(Path(args.inventory), args.case_id, args.description, args.container, args.seal, args.location, args.holder, args.notes), indent=2)); return 0
    if args.cmd == "update": print(json.dumps(update(Path(args.inventory), args.item_id, args.location, args.holder, args.status, args.notes), indent=2)); return 0
    print(json.dumps(read(Path(args.inventory)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
