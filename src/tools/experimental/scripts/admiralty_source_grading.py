#!/usr/bin/env python3
"""Admiralty 6x6 Source Grading.

Batch grades claims from a CSV using reliability and credibility columns, then
adds labels and use recommendations.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

REL = {"A": "completely reliable", "B": "usually reliable", "C": "fairly reliable", "D": "not usually reliable", "E": "unreliable", "F": "cannot judge"}
CRE = {"1": "confirmed", "2": "probably true", "3": "possibly true", "4": "doubtful", "5": "improbable", "6": "cannot judge"}


def recommendation(r: str, c: str) -> str:
    score = (ord(r) - ord("A")) + (int(c) - 1)
    return "accept" if score <= 3 else "corroborate" if score <= 6 else "review_before_use"


def process(input_csv: Path, output_csv: Path, rel_col: str, cred_col: str) -> dict:
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    for field in ["combined_grade", "reliability_label", "credibility_label", "recommendation"]:
        if field not in fields: fields.append(field)
    findings = []
    for idx, row in enumerate(rows, 1):
        r = str(row.get(rel_col, "F")).upper(); c = str(row.get(cred_col, "6"))
        if r not in REL or c not in CRE:
            findings.append({"row": idx, "issue": "invalid grade"}); r, c = "F", "6"
        row["combined_grade"] = r + c; row["reliability_label"] = REL[r]; row["credibility_label"] = CRE[c]; row["recommendation"] = recommendation(r, c)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output_csv), "rows": len(rows), "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch apply Admiralty 6x6 grading labels.")
    parser.add_argument("input_csv")
    parser.add_argument("--reliability-col", default="reliability")
    parser.add_argument("--credibility-col", default="credibility")
    parser.add_argument("--output", default="admiralty_graded.csv")
    args = parser.parse_args()
    print(json.dumps(process(Path(args.input_csv), Path(args.output), args.reliability_col, args.credibility_col), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
