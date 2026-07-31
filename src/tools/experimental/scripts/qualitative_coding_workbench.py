#!/usr/bin/env python3
"""NVivo / ATLAS.ti / MAXQDA qualitative analysis helper.

Creates a lightweight local coding workbook from text excerpts, applies keyword
seed codes, and exports code frequencies for review.
"""
from __future__ import annotations
import argparse, csv, json, re
from collections import Counter
from pathlib import Path


def read_texts(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for idx, paragraph in enumerate([p.strip() for p in text.split("\n") if p.strip()], 1):
            rows.append({"document": str(path), "excerpt_id": f"{path.stem}_{idx}", "excerpt": paragraph, "codes": "", "memo": ""})
    return rows


def apply_codes(rows: list[dict], code_terms: dict[str, list[str]]) -> list[dict]:
    for row in rows:
        text = row["excerpt"].lower()
        hits = [code for code, terms in code_terms.items() if any(term.lower() in text for term in terms)]
        row["codes"] = ";".join(sorted(hits))
    return rows


def parse_code_terms(items: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for item in items:
        if "=" not in item:
            raise ValueError("seed code must be code=term1,term2")
        code, terms = item.split("=", 1)
        out[code] = [t.strip() for t in terms.split(",") if t.strip()]
    return out


def export(rows: list[dict], output_csv: Path, summary_json: Path) -> dict:
    fields = ["document", "excerpt_id", "excerpt", "codes", "memo"]
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    counter = Counter(code for row in rows for code in row.get("codes", "").split(";") if code)
    summary = {"excerpts": len(rows), "code_counts": dict(counter)}
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return {"output_csv": str(output_csv), "summary_json": str(summary_json), **summary}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a lightweight qualitative coding workbook.")
    parser.add_argument("texts", nargs="+")
    parser.add_argument("--seed-code", action="append", default=[])
    parser.add_argument("--output", default="qualitative_coding.csv")
    parser.add_argument("--summary", default="qualitative_code_summary.json")
    args = parser.parse_args()
    rows = apply_codes(read_texts([Path(p) for p in args.texts]), parse_code_terms(args.seed_code))
    print(json.dumps(export(rows, Path(args.output), Path(args.summary)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
