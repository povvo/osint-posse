#!/usr/bin/env python3
"""Maintaining the Dissemination Log.

Records releases of reports, datasets, or extracts with recipient, version,
handling note, and acknowledgement status.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["release_id", "time_utc", "item", "item_sha256", "version", "recipient", "purpose", "handling", "acknowledged", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def add(log: Path, item: Path, version: str, recipient: str, purpose: str, handling: str, notes: str) -> dict:
    rows = read(log)
    record = {"release_id": str(uuid.uuid4()), "time_utc": now(), "item": str(item), "item_sha256": sha(item) if item.exists() and item.is_file() else "", "version": version, "recipient": recipient, "purpose": purpose, "handling": handling, "acknowledged": "no", "notes": notes}
    rows.append(record); write(log, rows); return record


def acknowledge(log: Path, release_id: str) -> dict:
    rows = read(log)
    for row in rows:
        if row["release_id"].startswith(release_id):
            row["acknowledged"] = "yes"; write(log, rows); return row
    raise KeyError(release_id)


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain a dissemination/release log.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("log"); a.add_argument("--item", required=True); a.add_argument("--version", default="1"); a.add_argument("--recipient", required=True); a.add_argument("--purpose", required=True); a.add_argument("--handling", default="standard"); a.add_argument("--notes", default="")
    k = sub.add_parser("ack"); k.add_argument("log"); k.add_argument("release_id")
    l = sub.add_parser("list"); l.add_argument("log")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add(Path(args.log), Path(args.item), args.version, args.recipient, args.purpose, args.handling, args.notes), indent=2)); return 0
    if args.cmd == "ack": print(json.dumps(acknowledge(Path(args.log), args.release_id), indent=2)); return 0
    print(json.dumps(read(Path(args.log)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
