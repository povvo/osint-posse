#!/usr/bin/env python3
"""Reverse image/video search log.

Records visual items, extracted frame paths, reverse-search services checked,
match URLs, and context notes. This script does not perform external searches.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["visual_id", "time_utc", "file_path", "sha256", "service", "query_note", "match_url", "match_context", "status", "reviewer"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
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


def add(log: Path, file_path: Path, service: str, query_note: str, match_url: str, context: str, status: str, reviewer: str) -> dict:
    rows = read(log)
    row = {"visual_id": str(uuid.uuid4()), "time_utc": now(), "file_path": str(file_path), "sha256": sha256(file_path), "service": service, "query_note": query_note, "match_url": match_url, "match_context": context, "status": status, "reviewer": reviewer}
    rows.append(row); write(log, rows); return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Maintain a reverse visual search review log.")
    parser.add_argument("log")
    parser.add_argument("--file", required=True)
    parser.add_argument("--service", required=True)
    parser.add_argument("--query-note", default="")
    parser.add_argument("--match-url", default="")
    parser.add_argument("--context", default="")
    parser.add_argument("--status", default="pending")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(); path = Path(args.log)
    if args.list:
        print(json.dumps(read(path), indent=2)); return 0
    print(json.dumps(add(path, Path(args.file), args.service, args.query_note, args.match_url, args.context, args.status, args.reviewer), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
