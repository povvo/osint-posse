#!/usr/bin/env python3
"""Barcode/label printing and inventory scanner.

Creates evidence labels, QR/barcode payload text, and an inventory CSV suitable
for label printing or scanner reconciliation.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["item_id", "case_id", "label", "container", "location", "created_utc", "barcode_payload", "status", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def add_item(path: Path, case_id: str, label: str, container: str, location: str, notes: str = "") -> dict:
    rows = load(path)
    item_id = f"EV-{uuid.uuid4().hex[:10].upper()}"
    payload = json.dumps({"case_id": case_id, "item_id": item_id}, separators=(",", ":"))
    row = {"item_id": item_id, "case_id": case_id, "label": label, "container": container, "location": location, "created_utc": now(), "barcode_payload": payload, "status": "in_inventory", "notes": notes}
    rows.append(row); save(path, rows); return row


def scan(path: Path, payload: str, location: str) -> dict:
    rows = load(path)
    data = json.loads(payload)
    for row in rows:
        if row["item_id"] == data.get("item_id") and row["case_id"] == data.get("case_id"):
            row["location"] = location; row["status"] = "scanned"; save(path, rows); return row
    raise KeyError("payload not found in inventory")


def labels(path: Path, output: Path) -> dict:
    rows = load(path)
    lines = []
    for row in rows:
        lines += ["---", f"CASE: {row['case_id']}", f"ITEM: {row['item_id']}", f"LABEL: {row['label']}", f"PAYLOAD: {row['barcode_payload']}"]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"labels": len(rows), "output": str(output)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create and reconcile evidence label inventory records.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add"); add.add_argument("inventory"); add.add_argument("--case-id", required=True); add.add_argument("--label", required=True); add.add_argument("--container", default=""); add.add_argument("--location", default=""); add.add_argument("--notes", default="")
    scn = sub.add_parser("scan"); scn.add_argument("inventory"); scn.add_argument("payload"); scn.add_argument("--location", required=True)
    lab = sub.add_parser("labels"); lab.add_argument("inventory"); lab.add_argument("--output", default="labels.txt")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add_item(Path(args.inventory), args.case_id, args.label, args.container, args.location, args.notes), indent=2)); return 0
    if args.cmd == "scan": print(json.dumps(scan(Path(args.inventory), args.payload, args.location), indent=2)); return 0
    print(json.dumps(labels(Path(args.inventory), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
