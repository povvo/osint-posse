#!/usr/bin/env python3
"""Admiralty 6x6 source grading matrix.

Creates a 6x6 grading matrix and optionally scores rows from a CSV. Intended for
reviewing source reliability and information credibility before synthesis.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

RELIABILITY = list("ABCDEF")
CREDIBILITY = list("123456")


def recommendation(r: str, c: str) -> str:
    score = (ord(r) - ord("A")) + (int(c) - 1)
    if score <= 2: return "strong"
    if score <= 5: return "usable_with_caveat"
    if score <= 8: return "corroborate_first"
    return "weak_or_unknown"


def matrix() -> list[dict]:
    return [{"reliability": r, "credibility": c, "grade": r + c, "recommendation": recommendation(r, c)} for r in RELIABILITY for c in CREDIBILITY]


def score_csv(input_csv: Path, output_csv: Path, rel_col: str, cred_col: str) -> dict:
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    for field in ["grade", "matrix_recommendation"]:
        if field not in fields: fields.append(field)
    for row in rows:
        r, c = str(row.get(rel_col, "F")).upper(), str(row.get(cred_col, "6"))
        if r not in RELIABILITY: r = "F"
        if c not in CREDIBILITY: c = "6"
        row["grade"] = r + c
        row["matrix_recommendation"] = recommendation(r, c)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output_csv), "rows": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or apply an Admiralty 6x6 grading matrix.")
    parser.add_argument("--matrix-output")
    parser.add_argument("--score-csv")
    parser.add_argument("--output", default="admiralty_matrix_scores.csv")
    parser.add_argument("--reliability-col", default="reliability")
    parser.add_argument("--credibility-col", default="credibility")
    args = parser.parse_args()
    if args.matrix_output:
        Path(args.matrix_output).write_text(json.dumps(matrix(), indent=2), encoding="utf-8")
    result = {"matrix_cells": 36}
    if args.score_csv:
        result.update(score_csv(Path(args.score_csv), Path(args.output), args.reliability_col, args.credibility_col))
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
