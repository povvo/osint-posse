#!/usr/bin/env python3
"""Content Verification Deep Pass.

Reviews a local text file for claim-like lines, dates, questions, and source
markers. Produces a structured CSV for manual verification.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

CLAIM_WORDS = re.compile(r"\b(is|are|was|were|shows|indicates|states|reports)\b", re.I)
DATE_TEXT = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def review(path: Path, output: Path) -> dict:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        text = line.strip()
        if not text:
            continue
        selected = CLAIM_WORDS.search(text) or DATE_TEXT.search(text) or text.endswith("?") or "source" in text.lower()
        if selected:
            rows.append({"line": line_no, "text": text, "claim_like": bool(CLAIM_WORDS.search(text)), "dates": ";".join(DATE_TEXT.findall(text)), "question": text.endswith("?"), "verification_status": "pending", "notes": ""})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["line", "text", "claim_like", "dates", "question", "verification_status", "notes"])
        writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "review_rows": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Review local text for verification items.")
    parser.add_argument("text_file")
    parser.add_argument("--output", default="content_verification.csv")
    args = parser.parse_args()
    print(json.dumps(review(Path(args.text_file), Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
