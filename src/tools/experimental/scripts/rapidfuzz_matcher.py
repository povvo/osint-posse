#!/usr/bin/env python3
"""RapidFuzz matcher.

Performs fuzzy matching between two CSV tables. Uses RapidFuzz when installed and
falls back to a built-in Levenshtein ratio otherwise.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b): a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]


def fallback_ratio(a: str, b: str) -> float:
    a, b = a.lower().strip(), b.lower().strip()
    if not a and not b: return 100.0
    return 100.0 * (1.0 - levenshtein(a, b) / max(len(a), len(b), 1))


def scorer():
    try:
        from rapidfuzz import fuzz  # type: ignore
        return lambda a, b: float(fuzz.WRatio(a, b)), "rapidfuzz"
    except Exception:
        return fallback_ratio, "fallback_levenshtein"


def match(left: Path, right: Path, left_col: str, right_col: str, threshold: float, limit: int) -> dict:
    left_rows, right_rows = read_csv(left), read_csv(right)
    score, engine = scorer(); matches = []
    for i, lrow in enumerate(left_rows, 1):
        candidates = []
        for j, rrow in enumerate(right_rows, 1):
            value = score(str(lrow.get(left_col, "")), str(rrow.get(right_col, "")))
            if value >= threshold: candidates.append({"right_row": j, "score": round(value, 2), "right": rrow})
        candidates.sort(key=lambda x: x["score"], reverse=True)
        if candidates: matches.append({"left_row": i, "left": lrow, "candidates": candidates[:limit]})
    return {"engine": engine, "left_rows": len(left_rows), "right_rows": len(right_rows), "matches": matches}


def main() -> int:
    ap = argparse.ArgumentParser(description="Fuzzy-match two CSV tables.")
    ap.add_argument("left_csv"); ap.add_argument("right_csv"); ap.add_argument("--left-col", required=True); ap.add_argument("--right-col", required=True); ap.add_argument("--threshold", type=float, default=85); ap.add_argument("--limit", type=int, default=3); ap.add_argument("--output")
    args = ap.parse_args()
    result = match(Path(args.left_csv), Path(args.right_csv), args.left_col, args.right_col, args.threshold, args.limit)
    if args.output: Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "matches"} | {"match_groups": len(result["matches"])}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
