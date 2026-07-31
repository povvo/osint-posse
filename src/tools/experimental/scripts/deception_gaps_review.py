#!/usr/bin/env python3
"""Addressing Deception and Gaps.

Reviews an ACH or findings table for missing evidence, single-source claims,
contradictions, and possible deception indicators.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

DECEPTION_TERMS = re.compile(r"\b(false|forged|altered|inconsistent|denied|retracted|anomaly|impossible)\b", re.I)


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def review(rows: list[dict], output: Path) -> dict:
    findings = []
    for idx, row in enumerate(rows, 1):
        text = " ".join(str(value) for value in row.values() if value)
        if not (row.get("source_ref") or row.get("source")):
            findings.append({"row": idx, "issue": "missing source reference"})
        if row.get("source_count") in {"1", 1}:
            findings.append({"row": idx, "issue": "single-source claim"})
        if DECEPTION_TERMS.search(text):
            findings.append({"row": idx, "issue": "deception_or_anomaly_term_present", "context": text[:300]})
        if not (row.get("gap") or row.get("open_question") or row.get("next_step")):
            findings.append({"row": idx, "issue": "no gap or next-step field"})
    report = {"rows": len(rows), "findings": findings, "finding_count": len(findings)}
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return {"output": str(output), "finding_count": len(findings)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Review table rows for deception indicators and evidence gaps.")
    parser.add_argument("input_csv")
    parser.add_argument("--output", default="deception_gap_review.json")
    args = parser.parse_args()
    print(json.dumps(review(read(Path(args.input_csv)), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
