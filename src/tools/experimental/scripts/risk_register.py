#!/usr/bin/env python3
"""Risk register.

Tracks operational, legal, safety, and evidential risks with likelihood, impact,
mitigation, owner, status, and review date.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import date, datetime, timezone
from pathlib import Path

FIELDS = ["risk_id", "created_utc", "category", "description", "likelihood", "impact", "score", "mitigation", "owner", "review_date", "status"]
STATUSES = {"open", "mitigating", "accepted", "closed"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def add(path: Path, category: str, description: str, likelihood: int, impact: int, mitigation: str, owner: str, review_date: str) -> dict:
    if not (1 <= likelihood <= 5 and 1 <= impact <= 5): raise ValueError("likelihood and impact must be 1..5")
    if review_date: date.fromisoformat(review_date)
    rows = read(path)
    row = {"risk_id": str(uuid.uuid4()), "created_utc": now(), "category": category, "description": description, "likelihood": likelihood, "impact": impact, "score": likelihood * impact, "mitigation": mitigation, "owner": owner, "review_date": review_date, "status": "open"}
    rows.append(row); write(path, rows); return row


def update(path: Path, risk_id: str, status: str) -> dict:
    if status not in STATUSES: raise ValueError(f"status must be one of {sorted(STATUSES)}")
    rows = read(path)
    for row in rows:
        if row["risk_id"].startswith(risk_id): row["status"] = status; write(path, rows); return row
    raise KeyError(risk_id)


def summary(path: Path) -> dict:
    rows = read(path)
    return {"count": len(rows), "open": sum(1 for r in rows if r.get("status") == "open"), "high": [r for r in rows if int(r.get("score") or 0) >= 15]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain a CSV risk register.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("register"); a.add_argument("--category", required=True); a.add_argument("--description", required=True); a.add_argument("--likelihood", type=int, required=True); a.add_argument("--impact", type=int, required=True); a.add_argument("--mitigation", default=""); a.add_argument("--owner", default=""); a.add_argument("--review-date", default="")
    u = sub.add_parser("update"); u.add_argument("register"); u.add_argument("risk_id"); u.add_argument("--status", required=True, choices=sorted(STATUSES))
    s = sub.add_parser("summary"); s.add_argument("register")
    l = sub.add_parser("list"); l.add_argument("register")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add(Path(args.register), args.category, args.description, args.likelihood, args.impact, args.mitigation, args.owner, args.review_date), indent=2)); return 0
    if args.cmd == "update": print(json.dumps(update(Path(args.register), args.risk_id, args.status), indent=2)); return 0
    print(json.dumps(summary(Path(args.register)) if args.cmd == "summary" else read(Path(args.register)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
