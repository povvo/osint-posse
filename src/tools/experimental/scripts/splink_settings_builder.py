#!/usr/bin/env python3
"""Splink settings builder.

Profiles a CSV and writes a starter Splink-style linkage settings JSON with
blocking rules, comparison columns, and field completeness metrics.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def completeness(rows: list[dict], field: str) -> float:
    if not rows: return 0.0
    return sum(1 for row in rows if str(row.get(field, "")).strip()) / len(rows)


def build_settings(rows: list[dict], unique_id: str, columns: list[str], blocking: list[str]) -> dict:
    comparisons = []
    for column in columns:
        comparisons.append({"output_column_name": column, "comparison_levels": [{"sql_condition": f"l.{column} = r.{column}", "label_for_charts": "exact match"}, {"sql_condition": "ELSE", "label_for_charts": "all other comparisons"}]})
    return {"link_type": "dedupe_only", "unique_id_column_name": unique_id, "blocking_rules_to_generate_predictions": [f"l.{b} = r.{b}" for b in blocking], "comparisons": comparisons, "field_profile": {c: {"completeness": completeness(rows, c)} for c in columns}}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create starter Splink linkage settings from a CSV.")
    ap.add_argument("csv")
    ap.add_argument("--unique-id", default="id")
    ap.add_argument("--column", action="append", required=True)
    ap.add_argument("--blocking", action="append", default=[])
    ap.add_argument("--output", default="splink_settings.json")
    args = ap.parse_args()
    rows = read_rows(Path(args.csv))
    settings = build_settings(rows, args.unique_id, args.column, args.blocking or args.column[:1])
    Path(args.output).write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "rows_profiled": len(rows), "comparisons": len(settings["comparisons"])}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
