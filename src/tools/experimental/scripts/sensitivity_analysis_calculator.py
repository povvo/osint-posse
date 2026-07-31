#!/usr/bin/env python3
"""Sensitivity analysis calculator.

Tests whether a conclusion score changes when low-quality or single-source rows
are removed from a CSV evidence table.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def score(rows: list[dict], score_col: str) -> float:
    total = 0.0
    for row in rows:
        try:
            total += float(row.get(score_col, 0) or 0)
        except ValueError:
            pass
    return total


def analyse(rows: list[dict], score_col: str, quality_col: str, source_count_col: str) -> dict:
    baseline = score(rows, score_col)
    without_low = [r for r in rows if str(r.get(quality_col, "")).lower() not in {"low", "weak", "f", "6"}]
    without_single = [r for r in rows if str(r.get(source_count_col, "1")).isdigit() and int(r.get(source_count_col, "1")) > 1]
    return {"baseline_score": baseline, "without_low_quality_score": score(without_low, score_col), "without_single_source_score": score(without_single, score_col), "baseline_rows": len(rows), "without_low_quality_rows": len(without_low), "without_single_source_rows": len(without_single)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run sensitivity checks on evidence score rows.")
    parser.add_argument("input_csv")
    parser.add_argument("--score-col", default="score")
    parser.add_argument("--quality-col", default="quality")
    parser.add_argument("--source-count-col", default="source_count")
    parser.add_argument("--output", default="sensitivity_analysis.json")
    args = parser.parse_args()
    result = analyse(read(Path(args.input_csv)), args.score_col, args.quality_col, args.source_count_col)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, **result}, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
