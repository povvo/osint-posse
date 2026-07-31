#!/usr/bin/env python3
"""Two-Mode Analysis.

Analyses bipartite source/target affiliations and projects them into one-mode
co-occurrence tables for both sides of the network.
"""
from __future__ import annotations
import argparse, csv, json, itertools
from collections import Counter, defaultdict
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def project(rows: list[dict], left_col: str, right_col: str) -> dict:
    left_to_right: dict[str, set[str]] = defaultdict(set)
    right_to_left: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        left, right = row.get(left_col, "").strip(), row.get(right_col, "").strip()
        if left and right:
            left_to_right[left].add(right); right_to_left[right].add(left)
    left_pairs, right_pairs = Counter(), Counter()
    for rights in left_to_right.values():
        for a, b in itertools.combinations(sorted(rights), 2): right_pairs[(a, b)] += 1
    for lefts in right_to_left.values():
        for a, b in itertools.combinations(sorted(lefts), 2): left_pairs[(a, b)] += 1
    return {"left_count": len(left_to_right), "right_count": len(right_to_left), "left_projection": [{"a": a, "b": b, "weight": w} for (a, b), w in left_pairs.items()], "right_projection": [{"a": a, "b": b, "weight": w} for (a, b), w in right_pairs.items()]}


def write_edges(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["a", "b", "weight"]); writer.writeheader(); writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run two-mode affiliation projection.")
    ap.add_argument("csv"); ap.add_argument("--left-col", required=True); ap.add_argument("--right-col", required=True); ap.add_argument("--output-dir", default="two_mode")
    args = ap.parse_args()
    result = project(read(Path(args.csv)), args.left_col, args.right_col)
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    write_edges(out / "left_projection.csv", result["left_projection"]); write_edges(out / "right_projection.csv", result["right_projection"])
    (out / "two_mode_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "left_count": result["left_count"], "right_count": result["right_count"]}, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
