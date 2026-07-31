#!/usr/bin/env python3
"""Dissemination log.

Records dissemination events, recipients, versions, handling restrictions, and
acknowledgement status.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["dissemination_id", "time_utc", "product", "sha256", "version", "recipient", "purpose", "handling", "acknowledged", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    if not path.exists() or not path.is_file(): return ""
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


def add(path: Path, product: Path, recipient: str, purpose: str, version: str, handling: str, notes: str) -> dict:
    rows = read(path)
    row = {"dissemination_id": str(uuid.uuid4()), "time_utc": now(), "product": str(product), "sha256": sha(product), "version": version, "recipient": recipient, "purpose": purpose, "handling": handling, "acknowledged": "no", "notes": notes}
    rows.append(row); write(path, rows); return row


def main() -> int:
    ap = argparse.ArgumentParser(description="Record dissemination events.")
    ap.add_argument("log"); ap.add_argument("--product", required=True); ap.add_argument("--recipient", required=True); ap.add_argument("--purpose", required=True); ap.add_argument("--version", default="1"); ap.add_argument("--handling", default="standard"); ap.add_argument("--notes", default=""); ap.add_argument("--list", action="store_true")
    args = ap.parse_args(); path = Path(args.log)
    if args.list: print(json.dumps(read(path), indent=2)); return 0
    print(json.dumps(add(path, Path(args.product), args.recipient, args.purpose, args.version, args.handling, args.notes), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
