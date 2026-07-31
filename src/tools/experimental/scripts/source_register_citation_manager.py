#!/usr/bin/env python3
"""Source register / citation manager.

Maintains a source register with stable IDs, citation fields, reliability notes,
and duplicate URL detection. Outputs JSON, CSV, and a Markdown bibliography.
"""
from __future__ import annotations
import argparse, csv, json, re, uuid
from datetime import datetime, timezone
from pathlib import Path

URL_RE = re.compile(r"^https?://", re.I)
SOURCE_TYPES = {"web", "document", "interview", "dataset", "archive", "other"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    csv_path = path.with_suffix(".csv")
    fields = ["id", "title", "source_type", "locator", "author", "publisher", "date", "accessed_utc", "reliability_note", "tags"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    write_markdown(path.with_suffix(".md"), rows)


def write_markdown(path: Path, rows: list[dict]) -> None:
    lines = ["# Source Register", ""]
    for row in rows:
        tag_text = ", ".join(row.get("tags", []))
        lines += [f"## {row['id']} · {row['title']}", "", f"- Type: {row['source_type']}", f"- Locator: {row['locator']}", f"- Author: {row.get('author','')}", f"- Publisher: {row.get('publisher','')}", f"- Date: {row.get('date','')}", f"- Accessed: {row['accessed_utc']}", f"- Reliability note: {row.get('reliability_note','')}", f"- Tags: {tag_text}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def add_source(path: Path, args: argparse.Namespace) -> dict:
    rows = load(path)
    if args.source_type not in SOURCE_TYPES:
        raise ValueError(f"source_type must be one of {sorted(SOURCE_TYPES)}")
    duplicate = next((r for r in rows if r.get("locator") == args.locator), None)
    row = {"id": duplicate["id"] if duplicate else str(uuid.uuid4()), "title": args.title, "source_type": args.source_type, "locator": args.locator, "author": args.author or "", "publisher": args.publisher or "", "date": args.date or "", "accessed_utc": now(), "reliability_note": args.reliability_note or "", "tags": args.tag or []}
    if duplicate:
        rows = [row if r["id"] == duplicate["id"] else r for r in rows]
    else:
        rows.append(row)
    save(path, rows)
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain a source register and citation export.")
    ap.add_argument("register")
    ap.add_argument("--title")
    ap.add_argument("--locator")
    ap.add_argument("--source-type", choices=sorted(SOURCE_TYPES), default="web")
    ap.add_argument("--author")
    ap.add_argument("--publisher")
    ap.add_argument("--date")
    ap.add_argument("--reliability-note")
    ap.add_argument("--tag", action="append")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    path = Path(args.register)
    if args.list:
        print(json.dumps(load(path), indent=2, ensure_ascii=False)); return 0
    if not args.title or not args.locator:
        ap.error("--title and --locator are required unless --list is used")
    print(json.dumps(add_source(path, args), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
