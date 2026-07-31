#!/usr/bin/env python3
"""Maintaining the Source Register.

Maintains source records, detects duplicate locators, records reliability and
credibility grades, and exports CSV, JSON, and Markdown views.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["source_id", "title", "locator", "source_type", "reliability", "credibility", "first_seen_utc", "last_reviewed_utc", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)
    path.with_suffix(".json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# Source Register", ""]
    for row in rows: lines += [f"## {row['source_id']} · {row['title']}", "", f"- Locator: {row['locator']}", f"- Type: {row['source_type']}", f"- Grade: {row['reliability']}{row['credibility']}", f"- Notes: {row['notes']}", ""]
    path.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")


def upsert(path: Path, title: str, locator: str, source_type: str, reliability: str, credibility: str, notes: str) -> dict:
    rows = read(path)
    existing = next((r for r in rows if r["locator"] == locator), None)
    if existing:
        existing.update({"title": title, "source_type": source_type, "reliability": reliability, "credibility": credibility, "last_reviewed_utc": now(), "notes": notes})
        row = existing
    else:
        row = {"source_id": str(uuid.uuid4()), "title": title, "locator": locator, "source_type": source_type, "reliability": reliability, "credibility": credibility, "first_seen_utc": now(), "last_reviewed_utc": now(), "notes": notes}
        rows.append(row)
    write(path, rows); return row


def main() -> int:
    ap = argparse.ArgumentParser(description="Add, update, or list source-register entries.")
    ap.add_argument("register")
    ap.add_argument("--title"); ap.add_argument("--locator"); ap.add_argument("--source-type", default="web")
    ap.add_argument("--reliability", default="F"); ap.add_argument("--credibility", default="6"); ap.add_argument("--notes", default="")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(); path = Path(args.register)
    if args.list: print(json.dumps(read(path), indent=2)); return 0
    if not args.title or not args.locator: ap.error("--title and --locator are required unless --list is used")
    print(json.dumps(upsert(path, args.title, args.locator, args.source_type, args.reliability, args.credibility, args.notes), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
