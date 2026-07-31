#!/usr/bin/env python3
"""Probabilistic Matching and Human Review.

Creates scored candidate pairs using normalised text overlap and outputs a review
CSV with blank reviewer decision fields.
"""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def tokens(value: str) -> set[str]:
    return {x.lower() for x in str(value).replace("-", " ").replace("/", " ").split() if x.strip()}


def score_pair(left: dict, right: dict, fields: list[str]) -> float:
    weights = []
    for field in fields:
        a, b = tokens(left.get(field, "")), tokens(right.get(field, ""))
        if not a and not b: continue
        jaccard = len(a & b) / max(len(a | b), 1)
        weights.append(jaccard)
    return sum(weights) / len(weights) if weights else 0.0


def candidate_pairs(left: list[dict], right: list[dict], fields: list[str], threshold: float, limit: int) -> list[dict]:
    pairs = []
    for i, lrow in enumerate(left, 1):
        for j, rrow in enumerate(right, 1):
            score = score_pair(lrow, rrow, fields)
            if score >= threshold:
                pairs.append({"left_row": i, "right_row": j, "score": round(score, 4), "review_decision": "", "reviewer": "", "notes": "", "left_record": json.dumps(lrow, ensure_ascii=False), "right_record": json.dumps(rrow, ensure_ascii=False)})
    pairs.sort(key=lambda row: (-row["score"], row["left_row"], row["right_row"]))
    return pairs[:limit]


def write_review(path: Path, rows: list[dict]) -> None:
    fields = ["left_row", "right_row", "score", "review_decision", "reviewer", "notes", "left_record", "right_record"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate probabilistic match candidates for human review.")
    ap.add_argument("left_csv"); ap.add_argument("right_csv"); ap.add_argument("--field", action="append", required=True)
    ap.add_argument("--threshold", type=float, default=0.35); ap.add_argument("--limit", type=int, default=500); ap.add_argument("--output", default="probabilistic_review.csv")
    args = ap.parse_args()
    rows = candidate_pairs(read_csv(Path(args.left_csv)), read_csv(Path(args.right_csv)), args.field, args.threshold, args.limit)
    write_review(Path(args.output), rows)
    print(json.dumps({"output": args.output, "candidate_pairs": len(rows), "threshold": args.threshold}, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
