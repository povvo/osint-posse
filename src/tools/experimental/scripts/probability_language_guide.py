#!/usr/bin/env python3
"""Probability-language guide.

Prints a standard probability-language table and reviews analytic text for vague
or non-standard likelihood wording.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

GUIDE = [
    {"term": "remote", "range": "1-5%"},
    {"term": "unlikely", "range": "20-45%"},
    {"term": "roughly even chance", "range": "45-55%"},
    {"term": "likely", "range": "55-80%"},
    {"term": "very likely", "range": "80-95%"},
    {"term": "almost certain", "range": "95-99%"},
]
VAGUE = re.compile(r"\b(maybe|possibly|seems|clearly|obviously|sort of|kind of)\b", re.I)


def review(path: Path, output: Path) -> dict:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if VAGUE.search(line):
            rows.append({"line": line_no, "text": line.strip(), "issue": "vague probability wording"})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["line", "text", "issue"]); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "issues": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Show probability guide or review wording.")
    parser.add_argument("--guide", action="store_true")
    parser.add_argument("--review")
    parser.add_argument("--output", default="probability_language_issues.csv")
    args = parser.parse_args()
    if args.guide:
        print(json.dumps(GUIDE, indent=2)); return 0
    if not args.review: parser.error("use --guide or --review")
    print(json.dumps(review(Path(args.review), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
