#!/usr/bin/env python3
"""waybackpy capture log.

Maintains a local queue and result log for web-archive capture work. It prepares
URLs for a separate archive tool and records returned archive URLs.
"""
from __future__ import annotations
import argparse, csv, json, re, uuid
from datetime import datetime, timezone
from pathlib import Path

URL_RE = re.compile(r"^https?://", re.I)
FIELDS = ["request_id", "created_utc", "url", "status", "archive_url", "requested_by", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def queue(path: Path, url: str, requested_by: str, notes: str) -> dict:
    if not URL_RE.match(url): raise ValueError("url must start with http:// or https://")
    rows = read(path); row = {"request_id": str(uuid.uuid4()), "created_utc": now(), "url": url, "status": "queued", "archive_url": "", "requested_by": requested_by, "notes": notes}
    rows.append(row); write(path, rows); return row


def complete(path: Path, request_id: str, archive_url: str) -> dict:
    rows = read(path)
    for row in rows:
        if row["request_id"].startswith(request_id):
            row["status"] = "captured"; row["archive_url"] = archive_url; write(path, rows); return row
    raise KeyError(request_id)


def export_queue(path: Path) -> dict:
    rows = read(path)
    return {"queued": [r["url"] for r in rows if r["status"] == "queued"], "captured": sum(1 for r in rows if r["status"] == "captured"), "total": len(rows)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Track web archive capture requests and results.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("queue"); q.add_argument("log"); q.add_argument("url"); q.add_argument("--requested-by", default="analyst"); q.add_argument("--notes", default="")
    c = sub.add_parser("complete"); c.add_argument("log"); c.add_argument("request_id"); c.add_argument("archive_url")
    l = sub.add_parser("list"); l.add_argument("log")
    args = ap.parse_args()
    if args.cmd == "queue": print(json.dumps(queue(Path(args.log), args.url, args.requested_by, args.notes), indent=2)); return 0
    if args.cmd == "complete": print(json.dumps(complete(Path(args.log), args.request_id, args.archive_url), indent=2)); return 0
    print(json.dumps(export_queue(Path(args.log)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
