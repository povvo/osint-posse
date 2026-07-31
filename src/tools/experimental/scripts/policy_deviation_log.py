#!/usr/bin/env python3
"""Real-Time Policy Deviation Logging.

Records policy deviations, urgency basis, authorisation, mitigation, and review
status in a CSV ledger.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["deviation_id", "time_utc", "case_id", "policy_ref", "deviation", "urgency_basis", "authorised_by", "mitigation", "status", "reviewer", "review_notes"]
STATUSES = {"open", "approved", "rejected", "closed"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def add(path: Path, args: argparse.Namespace) -> dict:
    rows = read(path)
    row = {"deviation_id": str(uuid.uuid4()), "time_utc": now(), "case_id": args.case_id, "policy_ref": args.policy_ref, "deviation": args.deviation, "urgency_basis": args.urgency_basis, "authorised_by": args.authorised_by, "mitigation": args.mitigation, "status": "open", "reviewer": "", "review_notes": ""}
    rows.append(row); write(path, rows); return row


def review(path: Path, deviation_id: str, status: str, reviewer: str, notes: str) -> dict:
    if status not in STATUSES: raise ValueError(f"status must be one of {sorted(STATUSES)}")
    rows = read(path)
    for row in rows:
        if row["deviation_id"].startswith(deviation_id):
            row["status"] = status; row["reviewer"] = reviewer; row["review_notes"] = notes; write(path, rows); return row
    raise KeyError(deviation_id)


def main() -> int:
    ap = argparse.ArgumentParser(description="Record and review policy deviations.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("log"); a.add_argument("--case-id", required=True); a.add_argument("--policy-ref", required=True); a.add_argument("--deviation", required=True); a.add_argument("--urgency-basis", required=True); a.add_argument("--authorised-by", default=""); a.add_argument("--mitigation", default="")
    r = sub.add_parser("review"); r.add_argument("log"); r.add_argument("deviation_id"); r.add_argument("--status", required=True, choices=sorted(STATUSES)); r.add_argument("--reviewer", required=True); r.add_argument("--notes", default="")
    l = sub.add_parser("list"); l.add_argument("log")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add(Path(args.log), args), indent=2)); return 0
    if args.cmd == "review": print(json.dumps(review(Path(args.log), args.deviation_id, args.status, args.reviewer, args.notes), indent=2)); return 0
    print(json.dumps(read(Path(args.log)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
