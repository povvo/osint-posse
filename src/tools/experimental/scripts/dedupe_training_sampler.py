#!/usr/bin/env python3
"""dedupe training sampler.

Creates candidate record pairs for human review before using a dedupe workflow.
It blocks by selected fields and scores simple token overlap for prioritisation.
"""
from __future__ import annotations
import argparse, csv, json, itertools
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def tokens(value: str) -> set[str]:
    return {part.lower() for part in str(value).replace("/", " ").replace("-", " ").split() if part.strip()}


def similarity(a: dict, b: dict, fields: list[str]) -> float:
    scores = []
    for field in fields:
        left, right = tokens(a.get(field, "")), tokens(b.get(field, ""))
        if not left and not right: continue
        scores.append(len(left & right) / max(1, len(left | right)))
    return sum(scores) / len(scores) if scores else 0.0


def sample_pairs(rows: list[dict], fields: list[str], block_field: str | None, limit: int) -> list[dict]:
    buckets: dict[str, list[dict]] = {}
    if block_field:
        for row in rows: buckets.setdefault(str(row.get(block_field, "")).lower()[:6], []).append(row)
    else:
        buckets = {"all": rows}
    pairs = []
    for group in buckets.values():
        for left, right in itertools.combinations(group, 2):
            score = similarity(left, right, fields)
            if score > 0:
                pairs.append({"score": round(score, 4), "left": left, "right": right, "review_label": ""})
    pairs.sort(key=lambda p: p["score"], reverse=True)
    return pairs[:limit]


def main() -> int:
    ap = argparse.ArgumentParser(description="Create candidate duplicate pairs for review.")
    ap.add_argument("csv")
    ap.add_argument("--field", action="append", required=True)
    ap.add_argument("--block-field")
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--output", default="dedupe_review_pairs.json")
    args = ap.parse_args()
    pairs = sample_pairs(read_rows(Path(args.csv)), args.field, args.block_field, args.limit)
    Path(args.output).write_text(json.dumps(pairs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": args.output, "pairs": len(pairs)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
