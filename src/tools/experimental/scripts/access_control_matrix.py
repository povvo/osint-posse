#!/usr/bin/env python3
"""Access-control matrix.

Builds and validates a read/write/export/approve matrix for roles and data
classes. Flags missing owners and conflicting permissions.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

PERMS = ["read", "write", "export", "approve", "admin"]


def load(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def normalise(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "allow", "allowed"}


def validate(rows: list[dict]) -> dict:
    findings = []
    for idx, row in enumerate(rows, 1):
        role = row.get("role", "").strip()
        data_class = row.get("data_class", "").strip()
        if not role: findings.append({"row": idx, "issue": "missing role"})
        if not data_class: findings.append({"row": idx, "issue": "missing data_class"})
        flags = {perm: normalise(row.get(perm, "")) for perm in PERMS}
        if flags["admin"] and not flags["approve"]:
            findings.append({"row": idx, "issue": "admin without approve"})
        if flags["export"] and not flags["read"]:
            findings.append({"row": idx, "issue": "export without read"})
        if flags["write"] and not flags["read"]:
            findings.append({"row": idx, "issue": "write without read"})
    return {"rows": len(rows), "ok": not findings, "findings": findings}


def init_template(output: Path) -> None:
    rows = [
        {"role": "analyst", "data_class": "standard", "read": "yes", "write": "yes", "export": "no", "approve": "no", "admin": "no", "owner": "case_manager"},
        {"role": "reviewer", "data_class": "standard", "read": "yes", "write": "no", "export": "yes", "approve": "yes", "admin": "no", "owner": "case_manager"},
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["role", "data_class", *PERMS, "owner"])
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or validate an access-control matrix CSV.")
    ap.add_argument("--init")
    ap.add_argument("--validate")
    args = ap.parse_args()
    if args.init:
        init_template(Path(args.init)); print(json.dumps({"created": args.init}, indent=2)); return 0
    if not args.validate: ap.error("use --init or --validate")
    print(json.dumps(validate(load(Path(args.validate))), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
