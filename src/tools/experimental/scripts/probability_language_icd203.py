#!/usr/bin/env python3
"""Applying Standardised Probability Language (ICD 203).

Normalises confidence and likelihood phrases in analytic text and produces a
review report for non-standard probability language.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

TERMS = {
    "remote": (1, 5), "unlikely": (20, 45), "roughly even chance": (45, 55),
    "likely": (55, 80), "very likely": (80, 95), "almost certain": (95, 99),
}
VAGUE = re.compile(r"\b(maybe|possibly|could be|seems|feels like|sort of|kind of)\b", re.I)


def scan(path: Path, output: Path) -> dict:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        lower = line.lower()
        matched = [term for term in TERMS if term in lower]
        vague = bool(VAGUE.search(line))
        if matched or vague:
            rows.append({"line": line_no, "text": line.strip(), "standard_terms": ";".join(matched), "vague_language": vague, "recommendation": "replace vague wording" if vague else "ok"})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["line", "text", "standard_terms", "vague_language", "recommendation"]); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "review_items": len(rows), "vague_items": sum(1 for r in rows if r["vague_language"])}


def print_terms() -> dict:
    return {term: {"range_percent": rng} for term, rng in TERMS.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description="Review probability language in analytic text.")
    ap.add_argument("--input")
    ap.add_argument("--output", default="probability_language_review.csv")
    ap.add_argument("--terms", action="store_true")
    args = ap.parse_args()
    if args.terms: print(json.dumps(print_terms(), indent=2)); return 0
    if not args.input: ap.error("--input is required unless --terms is used")
    print(json.dumps(scan(Path(args.input), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
