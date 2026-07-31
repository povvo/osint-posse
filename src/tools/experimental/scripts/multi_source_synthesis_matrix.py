#!/usr/bin/env python3
"""Multi-source synthesis matrix.

Compares claims across source types, grades, and confidence levels so synthesis
can separate corroborated claims from single-source claims.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict, Counter
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def synthesize(rows: list[dict], claim_col: str, source_type_col: str, confidence_col: str) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        claim = " ".join(str(row.get(claim_col, "")).lower().split())
        if claim:
            grouped[claim].append(row)
    matrix = []
    for claim, items in grouped.items():
        source_types = Counter(row.get(source_type_col, "unknown") or "unknown" for row in items)
        confidences = Counter(row.get(confidence_col, "unknown") or "unknown" for row in items)
        matrix.append({"claim": claim, "source_count": len(items), "source_types": dict(source_types), "confidence_values": dict(confidences), "synthesis_status": "multi_source" if len(source_types) >= 2 else "single_source"})
    return {"claim_count": len(matrix), "multi_source_claims": sum(1 for m in matrix if m["synthesis_status"] == "multi_source"), "matrix": matrix}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a multi-source synthesis matrix from claim rows.")
    parser.add_argument("claims_csv")
    parser.add_argument("--claim-col", default="claim")
    parser.add_argument("--source-type-col", default="source_type")
    parser.add_argument("--confidence-col", default="confidence")
    parser.add_argument("--output", default="multi_source_synthesis.json")
    args = parser.parse_args()
    report = synthesize(read(Path(args.claims_csv)), args.claim_col, args.source_type_col, args.confidence_col)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "claim_count": report["claim_count"], "multi_source_claims": report["multi_source_claims"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
