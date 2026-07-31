#!/usr/bin/env python3
"""Parallel Sourcing and Corroboration.

Compares claims across source rows and reports whether each claim is corroborated
by two or more independent source groups.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def norm(value: str) -> str:
    return " ".join(str(value).lower().split())


def assess(rows: list[dict], claim_col: str, source_col: str, group_col: str | None) -> dict:
    claims: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        claim = norm(row.get(claim_col, ""))
        if claim:
            claims[claim].append(row)
    report = []
    for claim, items in claims.items():
        groups = {row.get(group_col, row.get(source_col, "")) for row in items} if group_col else {row.get(source_col, "") for row in items}
        report.append({"claim": claim, "source_count": len(items), "independent_groups": len({g for g in groups if g}), "corroborated": len({g for g in groups if g}) >= 2, "sources": [row.get(source_col, "") for row in items]})
    return {"claim_count": len(report), "corroborated": sum(1 for row in report if row["corroborated"]), "claims": report}


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess corroboration across parallel sources.")
    parser.add_argument("claims_csv")
    parser.add_argument("--claim-col", default="claim")
    parser.add_argument("--source-col", default="source")
    parser.add_argument("--group-col")
    parser.add_argument("--output", default="corroboration_report.json")
    args = parser.parse_args()
    result = assess(read_rows(Path(args.claims_csv)), args.claim_col, args.source_col, args.group_col)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "claim_count": result["claim_count"], "corroborated": result["corroborated"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
