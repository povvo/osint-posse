#!/usr/bin/env python3
"""Claim review spreadsheet.

Creates or enriches a claim-review CSV with source, repeated-claim marker,
contradiction marker, confidence, reviewer, and status fields.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path

FIELDS = ["claim_id", "claim", "source", "original_source", "repeat_count", "contradiction", "confidence", "reviewer", "status", "notes"]


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def create(output: Path) -> dict:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    return {"created": str(output), "fields": FIELDS}


def enrich(input_csv: Path, output_csv: Path, claim_col: str, source_col: str) -> dict:
    rows = read(input_csv)
    counts = Counter(" ".join(str(row.get(claim_col, "")).lower().split()) for row in rows)
    out = []
    for idx, row in enumerate(rows, 1):
        key = " ".join(str(row.get(claim_col, "")).lower().split())
        out.append({"claim_id": row.get("claim_id") or f"C{idx:04d}", "claim": row.get(claim_col, ""), "source": row.get(source_col, ""), "original_source": row.get("original_source", ""), "repeat_count": counts[key], "contradiction": row.get("contradiction", ""), "confidence": row.get("confidence", ""), "reviewer": row.get("reviewer", ""), "status": row.get("status", "pending"), "notes": row.get("notes", "")})
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(out)
    return {"output": str(output_csv), "claims": len(out), "repeated_claims": sum(1 for r in out if int(r["repeat_count"]) > 1)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or enrich a claim-review spreadsheet.")
    parser.add_argument("--create")
    parser.add_argument("--input")
    parser.add_argument("--output", default="claim_review.csv")
    parser.add_argument("--claim-col", default="claim")
    parser.add_argument("--source-col", default="source")
    args = parser.parse_args()
    if args.create:
        print(json.dumps(create(Path(args.create)), indent=2)); return 0
    if not args.input:
        parser.error("use --create or --input")
    print(json.dumps(enrich(Path(args.input), Path(args.output), args.claim_col, args.source_col), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
