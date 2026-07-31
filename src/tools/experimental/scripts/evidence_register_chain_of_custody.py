#!/usr/bin/env python3
"""Evidence register and chain-of-custody log.

Registers items, records transfers, and verifies custody continuity in a local CSV
ledger.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["event_id", "item_id", "time_utc", "event", "handler_from", "handler_to", "location", "file_path", "sha256", "notes"]
EVENTS = {"register", "transfer", "check", "release"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    if not path.exists() or not path.is_file(): return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rows(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(data)


def add_event(log: Path, item_id: str, event: str, handler_from: str, handler_to: str, location: str, file_path: str, notes: str) -> dict:
    if event not in EVENTS: raise ValueError(f"event must be one of {sorted(EVENTS)}")
    data = rows(log)
    item_id = item_id or str(uuid.uuid4())
    record = {"event_id": str(uuid.uuid4()), "item_id": item_id, "time_utc": now(), "event": event, "handler_from": handler_from, "handler_to": handler_to, "location": location, "file_path": file_path, "sha256": sha(Path(file_path)) if file_path else "", "notes": notes}
    data.append(record); write(log, data); return record


def continuity(log: Path) -> dict:
    data = rows(log); findings = []
    by_item: dict[str, list[dict]] = {}
    for row in data: by_item.setdefault(row["item_id"], []).append(row)
    for item_id, events in by_item.items():
        events.sort(key=lambda r: r["time_utc"])
        holder = ""
        for event in events:
            if event["event"] == "register": holder = event["handler_to"]
            elif event["event"] == "transfer":
                if holder and event["handler_from"] != holder: findings.append({"item_id": item_id, "event_id": event["event_id"], "issue": "transfer from does not match current holder"})
                holder = event["handler_to"]
    return {"items": len(by_item), "events": len(data), "ok": not findings, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain an evidence register and custody ledger.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("event"); a.add_argument("log"); a.add_argument("--item-id", default=""); a.add_argument("--event", required=True, choices=sorted(EVENTS)); a.add_argument("--from", dest="handler_from", default=""); a.add_argument("--to", dest="handler_to", required=True); a.add_argument("--location", default=""); a.add_argument("--file", default=""); a.add_argument("--notes", default="")
    c = sub.add_parser("check"); c.add_argument("log")
    l = sub.add_parser("list"); l.add_argument("log")
    args = ap.parse_args()
    if args.cmd == "event": print(json.dumps(add_event(Path(args.log), args.item_id, args.event, args.handler_from, args.handler_to, args.location, args.file, args.notes), indent=2)); return 0
    if args.cmd == "check": print(json.dumps(continuity(Path(args.log)), indent=2)); return 0
    print(json.dumps(rows(Path(args.log)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
