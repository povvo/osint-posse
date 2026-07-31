#!/usr/bin/env python3
"""Deterministic Matching for Unique Identifiers.

Matches two CSV tables by exact normalised identifier columns and reports matched,
unmatched-left, and unmatched-right records.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def norm(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", str(value)).upper()


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = sorted({key for row in rows for key in row}) if rows else ["status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def match(left: list[dict], right: list[dict], left_col: str, right_col: str) -> dict:
    index: dict[str, list[dict]] = {}
    for row in right:
        key = norm(row.get(right_col, ""))
        if key: index.setdefault(key, []).append(row)
    matched, unmatched_left, used_right = [], [], set()
    for i, row in enumerate(left, 1):
        key = norm(row.get(left_col, ""))
        hits = index.get(key, [])
        if hits:
            for hit in hits:
                used_right.add(id(hit)); matched.append({"left_row": i, "match_key": key, "left": row, "right": hit})
        else:
            unmatched_left.append(row)
    unmatched_right = [row for row in right if id(row) not in used_right]
    return {"matched": matched, "unmatched_left": unmatched_left, "unmatched_right": unmatched_right}


def main() -> int:
    ap = argparse.ArgumentParser(description="Exact-match two CSVs by identifier columns.")
    ap.add_argument("left_csv"); ap.add_argument("right_csv"); ap.add_argument("--left-col", required=True); ap.add_argument("--right-col", required=True); ap.add_argument("--output-dir", default="deterministic_match")
    args = ap.parse_args()
    result = match(read_csv(Path(args.left_csv)), read_csv(Path(args.right_csv)), args.left_col, args.right_col)
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "matched.csv", result["matched"]); write_csv(out / "unmatched_left.csv", result["unmatched_left"]); write_csv(out / "unmatched_right.csv", result["unmatched_right"])
    summary = {"matched": len(result["matched"]), "unmatched_left": len(result["unmatched_left"]), "unmatched_right": len(result["unmatched_right"]), "output_dir": str(out)}
    print(json.dumps(summary, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
