#!/usr/bin/env python3
"""Key assumptions check.

Tracks assumptions, required evidence, failure indicators, and review status.
Outputs an assumption risk summary from a CSV register.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["assumption_id", "assumption", "must_hold_for", "evidence_required", "failure_indicator", "confidence", "status", "owner"]


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def init(output: Path) -> dict:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    return {"created": str(output), "fields": FIELDS}


def audit(path: Path) -> dict:
    rows = read(path); findings = []
    for idx, row in enumerate(rows, 1):
        if not row.get("evidence_required"): findings.append({"row": idx, "issue": "missing evidence_required"})
        if not row.get("failure_indicator"): findings.append({"row": idx, "issue": "missing failure_indicator"})
        if row.get("confidence", "").lower() == "high" and row.get("status", "").lower() != "tested": findings.append({"row": idx, "issue": "high-confidence assumption not marked tested"})
    return {"assumptions": len(rows), "findings": findings, "ok": not findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or audit a key assumptions register.")
    parser.add_argument("--init")
    parser.add_argument("--audit")
    args = parser.parse_args()
    if args.init: print(json.dumps(init(Path(args.init)), indent=2)); return 0
    if not args.audit: parser.error("use --init or --audit")
    print(json.dumps(audit(Path(args.audit)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
