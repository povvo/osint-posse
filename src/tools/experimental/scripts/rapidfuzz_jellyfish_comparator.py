#!/usr/bin/env python3
"""RapidFuzz / jellyfish comparator.

Combines fuzzy string similarity and phonetic keys for record comparison. Uses
optional libraries when present and safe built-in fallbacks otherwise.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def soundex(value: str) -> str:
    value = re.sub(r"[^A-Za-z]", "", value).upper()
    if not value: return ""
    code_map = {**dict.fromkeys("BFPV", "1"), **dict.fromkeys("CGJKQSXZ", "2"), **dict.fromkeys("DT", "3"), "L": "4", **dict.fromkeys("MN", "5"), "R": "6"}
    first, prev, out = value[0], code_map.get(value[0], ""), []
    for ch in value[1:]:
        code = code_map.get(ch, "")
        if code and code != prev: out.append(code)
        prev = code
    return (first + "".join(out) + "000")[:4]


def ratio(a: str, b: str) -> float:
    try:
        from rapidfuzz import fuzz  # type: ignore
        return float(fuzz.WRatio(a, b))
    except Exception:
        a, b = a.lower(), b.lower()
        common = sum(1 for ch in set(a) if ch in b)
        return 100.0 * common / max(len(set(a) | set(b)), 1)


def phonetic(value: str) -> str:
    try:
        import jellyfish  # type: ignore
        return jellyfish.soundex(value)
    except Exception:
        return soundex(value)


def compare(input_csv: Path, left_col: str, right_col: str, output: Path) -> dict:
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    out_rows = []
    for row in rows:
        left, right = str(row.get(left_col, "")), str(row.get(right_col, ""))
        out_rows.append({**row, "similarity": round(ratio(left, right), 2), "left_soundex": phonetic(left), "right_soundex": phonetic(right), "phonetic_match": phonetic(left) == phonetic(right) and bool(left and right)})
    fields = list(out_rows[0].keys()) if out_rows else ["similarity"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(out_rows)
    return {"rows": len(out_rows), "output": str(output)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare two text columns using fuzzy and phonetic keys.")
    ap.add_argument("input_csv"); ap.add_argument("--left-col", required=True); ap.add_argument("--right-col", required=True); ap.add_argument("--output", default="string_comparison.csv")
    args = ap.parse_args()
    print(json.dumps(compare(Path(args.input_csv), args.left_col, args.right_col, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
