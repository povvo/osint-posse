#!/usr/bin/env python3
"""Structural Separation of Facts, Assumptions, and Judgments.

Classifies report lines into fact, assumption, judgement, or question using
explicit markers and cautious keyword checks. Produces a review CSV.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

MARKERS = {"fact:": "fact", "assumption:": "assumption", "judgment:": "judgement", "judgement:": "judgement", "question:": "question"}
JUDGEMENT_WORDS = re.compile(r"\b(likely|probably|assess|suggests|indicates|appears)\b", re.I)


def classify(line: str) -> tuple[str, str]:
    stripped = line.strip()
    lower = stripped.lower()
    for marker, label in MARKERS.items():
        if lower.startswith(marker): return label, stripped[len(marker):].strip()
    if stripped.endswith("?"): return "question", stripped
    if JUDGEMENT_WORDS.search(stripped): return "judgement", stripped
    if re.search(r"\b(if|unless|assuming|provided that)\b", stripped, re.I): return "assumption", stripped
    return "fact_unverified", stripped


def process(input_file: Path, output_csv: Path) -> dict:
    rows = []
    for number, line in enumerate(input_file.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip(): continue
        kind, text = classify(line)
        rows.append({"line": number, "classification": kind, "text": text, "source_ref": "", "review_note": ""})
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["line", "classification", "text", "source_ref", "review_note"]); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output_csv), "rows": len(rows), "counts": {k: sum(1 for r in rows if r["classification"] == k) for k in sorted({r["classification"] for r in rows})}}


def main() -> int:
    ap = argparse.ArgumentParser(description="Separate facts, assumptions, judgements, and questions.")
    ap.add_argument("input_text"); ap.add_argument("--output", default="fact_assumption_judgement_review.csv")
    args = ap.parse_args()
    print(json.dumps(process(Path(args.input_text), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
