#!/usr/bin/env python3
"""Entity Resolution Pipeline (Fellegi-Sunter).

Scores candidate pairs using field agreement weights and emits match / review /
non-match decisions with an audit-friendly CSV output.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def parse_weight(items: list[str]) -> dict[str, float]:
    weights = {}
    for item in items:
        if "=" not in item: raise ValueError("weights must be field=value")
        field, value = item.split("=", 1); weights[field] = float(value)
    return weights


def field_agrees(left: str, right: str) -> bool:
    return left.strip().lower() == right.strip().lower() and bool(left.strip())


def compare(left_rows: list[dict], right_rows: list[dict], weights: dict[str, float], match_threshold: float, review_threshold: float) -> list[dict]:
    results = []
    for i, left in enumerate(left_rows, 1):
        for j, right in enumerate(right_rows, 1):
            score, agreements = 0.0, []
            for field, weight in weights.items():
                if field_agrees(str(left.get(field, "")), str(right.get(field, ""))):
                    score += weight; agreements.append(field)
            decision = "match" if score >= match_threshold else "review" if score >= review_threshold else "non_match"
            if decision != "non_match" or score > 0:
                results.append({"left_row": i, "right_row": j, "score": round(score, 4), "decision": decision, "agreements": ";".join(agreements)})
    return sorted(results, key=lambda r: (-r["score"], r["left_row"], r["right_row"]))


def write_results(path: Path, rows: list[dict]) -> None:
    fields = ["left_row", "right_row", "score", "decision", "agreements"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Score candidate entity matches with weighted field agreements.")
    ap.add_argument("left_csv"); ap.add_argument("right_csv"); ap.add_argument("--weight", action="append", required=True)
    ap.add_argument("--match-threshold", type=float, default=10.0); ap.add_argument("--review-threshold", type=float, default=4.0); ap.add_argument("--output", default="entity_resolution_scores.csv")
    args = ap.parse_args()
    scores = compare(read_csv(Path(args.left_csv)), read_csv(Path(args.right_csv)), parse_weight(args.weight), args.match_threshold, args.review_threshold)
    write_results(Path(args.output), scores)
    print(json.dumps({"output": args.output, "pairs_scored": len(scores), "matches": sum(1 for r in scores if r["decision"] == "match"), "review": sum(1 for r in scores if r["decision"] == "review")}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
