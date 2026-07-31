#!/usr/bin/env python3
"""OSINT Technical Verification.

Creates a local technical-verification checklist for public-source material:
locator, capture status, hash, metadata, visual review, and corroboration status.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["item_id", "locator", "capture_file", "sha256", "metadata_checked", "visual_checked", "archive_checked", "corroborated", "status", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def add(log: Path, locator: str, capture_file: str, notes: str) -> dict:
    rows = read(log)
    row = {"item_id": f"tech_{len(rows)+1:04d}", "locator": locator, "capture_file": capture_file, "sha256": digest(Path(capture_file)) if capture_file else "", "metadata_checked": "no", "visual_checked": "no", "archive_checked": "no", "corroborated": "no", "status": "pending", "notes": notes}
    rows.append(row); write(log, rows); return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Maintain a local technical verification checklist.")
    parser.add_argument("log")
    parser.add_argument("--locator")
    parser.add_argument("--capture-file", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    path = Path(args.log)
    if args.list:
        print(json.dumps(read(path), indent=2)); return 0
    if not args.locator:
        parser.error("--locator is required unless --list is used")
    print(json.dumps(add(path, args.locator, args.capture_file, args.notes), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
