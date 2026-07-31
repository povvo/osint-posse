#!/usr/bin/env python3
"""Assessing Diagnosticity and Matrix Scoring.

Scores ACH matrix rows and summarises which hypotheses are weakened by the most
inconsistent diagnostic evidence.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path

SCORES = {"consistent": 1, "neutral": 0, "inconsistent": -2, "very_inconsistent": -4, "unscored": 0}


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def summarise(rows: list[dict], output: Path) -> dict:
    totals: dict[str, float] = defaultdict(float)
    details: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        hyp = row.get("hypothesis_id") or row.get("hypothesis") or "unknown"
        score = SCORES.get(str(row.get("score", "unscored")).lower(), 0)
        try:
            weight = float(row.get("diagnosticity", 1) or 1)
        except ValueError:
            weight = 1
        value = score * weight
        totals[hyp] += value
        details[hyp].append({"evidence_id": row.get("evidence_id"), "score": row.get("score"), "weighted_value": value})
    result = {"hypotheses": [{"hypothesis": h, "total": totals[h], "rows": details[h]} for h in sorted(totals, key=totals.get, reverse=True)]}
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return {"output": str(output), "hypotheses": len(result["hypotheses"])}


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarise ACH matrix diagnosticity scores.")
    parser.add_argument("matrix_csv")
    parser.add_argument("--output", default="ach_score_summary.json")
    args = parser.parse_args()
    print(json.dumps(summarise(read(Path(args.matrix_csv)), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
