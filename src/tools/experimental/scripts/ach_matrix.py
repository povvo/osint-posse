#!/usr/bin/env python3
"""ACH matrix.

Maintains an Analysis of Competing Hypotheses matrix and checks whether every
hypothesis/evidence cell has been scored.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["evidence_id", "evidence", "hypothesis_id", "hypothesis", "score", "diagnosticity", "source_ref", "notes"]
VALID_SCORES = {"consistent", "neutral", "inconsistent", "very_inconsistent", "unscored"}


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def init(output: Path, hypotheses: list[str], evidence: list[str]) -> dict:
    rows = []
    for e_idx, e in enumerate(evidence, 1):
        for h_idx, h in enumerate(hypotheses, 1):
            rows.append({"evidence_id": f"E{e_idx}", "evidence": e, "hypothesis_id": f"H{h_idx}", "hypothesis": h, "score": "unscored", "diagnosticity": "", "source_ref": "", "notes": ""})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "rows": len(rows)}


def audit(path: Path) -> dict:
    rows = read(path); findings = []
    for idx, row in enumerate(rows, 1):
        if row.get("score") not in VALID_SCORES: findings.append({"row": idx, "issue": "invalid score"})
        if row.get("score") == "unscored": findings.append({"row": idx, "issue": "unscored cell"})
        if not row.get("source_ref"): findings.append({"row": idx, "issue": "missing source_ref"})
    return {"rows": len(rows), "ok": not findings, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or audit an ACH matrix CSV.")
    parser.add_argument("--init")
    parser.add_argument("--hypothesis", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--audit")
    args = parser.parse_args()
    if args.init:
        if not args.hypothesis or not args.evidence: parser.error("--hypothesis and --evidence required with --init")
        print(json.dumps(init(Path(args.init), args.hypothesis, args.evidence), indent=2)); return 0
    if not args.audit: parser.error("use --init or --audit")
    print(json.dumps(audit(Path(args.audit)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
