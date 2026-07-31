#!/usr/bin/env python3
"""jellyfish phonetic keys.

Adds phonetic and normalised-name keys to a CSV. Uses jellyfish if installed;
otherwise provides a compact Soundex fallback.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def soundex(name: str) -> str:
    name = re.sub(r"[^A-Za-z]", "", name).upper()
    if not name: return ""
    codes = {**dict.fromkeys("BFPV", "1"), **dict.fromkeys("CGJKQSXZ", "2"), **dict.fromkeys("DT", "3"), "L": "4", **dict.fromkeys("MN", "5"), "R": "6"}
    first, prev, out = name[0], codes.get(name[0], ""), []
    for ch in name[1:]:
        code = codes.get(ch, "")
        if code and code != prev: out.append(code)
        prev = code
    return (first + "".join(out) + "000")[:4]


def keyer():
    try:
        import jellyfish  # type: ignore
        return lambda value: {"soundex": jellyfish.soundex(value), "metaphone": jellyfish.metaphone(value)}, "jellyfish"
    except Exception:
        return lambda value: {"soundex": soundex(value), "metaphone": ""}, "fallback_soundex"


def process(input_csv: Path, column: str, output_csv: Path) -> dict:
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle)); fields = list(rows[0].keys()) if rows else []
    make_key, engine = keyer(); new_fields = fields + [f"{column}_normalised", f"{column}_soundex", f"{column}_metaphone"]
    for row in rows:
        value = str(row.get(column, ""))
        keys = make_key(value)
        row[f"{column}_normalised"] = re.sub(r"\s+", " ", value.strip().lower())
        row[f"{column}_soundex"] = keys["soundex"]
        row[f"{column}_metaphone"] = keys["metaphone"]
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=new_fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    return {"engine": engine, "rows": len(rows), "output": str(output_csv)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Add phonetic keys to a CSV column.")
    ap.add_argument("input_csv"); ap.add_argument("--column", required=True); ap.add_argument("--output", default="phonetic_keys.csv")
    args = ap.parse_args()
    print(json.dumps(process(Path(args.input_csv), args.column, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
