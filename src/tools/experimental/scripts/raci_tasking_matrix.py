#!/usr/bin/env python3
"""RACI/tasking matrix.

Creates and validates a RACI matrix for tasks, roles, approvals, and escalation
paths. Flags tasks without exactly one accountable role.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

VALID = {"R", "A", "C", "I", ""}


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def init(output: Path, roles: list[str]) -> dict:
    fields = ["task", *roles, "escalation", "notes"]
    rows = [{"task": "Example task", **{r: "A" if i == 0 else "R" if i == 1 else "C" for i, r in enumerate(roles)}, "escalation": roles[0] if roles else "", "notes": ""}]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    return {"created": str(output), "roles": roles}


def validate(path: Path) -> dict:
    rows = read(path); fields = [f for f in rows[0].keys() if f not in {"task", "escalation", "notes"}] if rows else []
    findings = []
    for idx, row in enumerate(rows, 1):
        accountable = [role for role in fields if row.get(role, "").strip().upper() == "A"]
        responsible = [role for role in fields if row.get(role, "").strip().upper() == "R"]
        for role in fields:
            if row.get(role, "").strip().upper() not in VALID: findings.append({"row": idx, "role": role, "issue": "invalid RACI value"})
        if len(accountable) != 1: findings.append({"row": idx, "task": row.get("task"), "issue": "must have exactly one accountable role"})
        if not responsible: findings.append({"row": idx, "task": row.get("task"), "issue": "no responsible role"})
    return {"rows": len(rows), "roles": fields, "ok": not findings, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or validate a RACI tasking matrix.")
    ap.add_argument("--init")
    ap.add_argument("--role", action="append", default=[])
    ap.add_argument("--validate")
    args = ap.parse_args()
    if args.init: print(json.dumps(init(Path(args.init), args.role), indent=2)); return 0
    if not args.validate: ap.error("use --init or --validate")
    print(json.dumps(validate(Path(args.validate)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
