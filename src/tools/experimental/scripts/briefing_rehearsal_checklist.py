#!/usr/bin/env python3
"""Briefing rehearsal checklist.

Creates a rehearsal checklist and validates that a briefing has questions,
caveats, confidence language, and decision asks prepared.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

CHECKS = ["bottom_line_clear", "source_summary_ready", "confidence_language_present", "caveats_prepared", "likely_questions_prepared", "decision_ask_clear", "fallback_slide_ready"]
CONFIDENCE = re.compile(r"\b(low|medium|high|likely|unlikely|confidence|almost certain)\b", re.I)


def create(output: Path) -> dict:
    rows = [{"check": check, "status": "pending", "owner": "", "notes": ""} for check in CHECKS]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "owner", "notes"]); writer.writeheader(); writer.writerows(rows)
    return {"created": str(output), "checks": len(rows)}


def review(briefing: Path, output: Path) -> dict:
    text = briefing.read_text(encoding="utf-8", errors="replace")
    rows = [
        {"check": "bottom_line_clear", "status": "pass" if "BLUF" in text or "Bottom Line" in text else "review", "notes": ""},
        {"check": "confidence_language_present", "status": "pass" if CONFIDENCE.search(text) else "review", "notes": ""},
        {"check": "caveats_prepared", "status": "pass" if "Caveat" in text else "review", "notes": ""},
        {"check": "decision_ask_clear", "status": "pass" if "Decision" in text else "review", "notes": ""},
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "notes"]); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "review_items": len(rows), "needs_review": sum(1 for r in rows if r["status"] == "review")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or run a briefing rehearsal checklist.")
    ap.add_argument("--create")
    ap.add_argument("--briefing")
    ap.add_argument("--output", default="briefing_rehearsal_review.csv")
    args = ap.parse_args()
    if args.create: print(json.dumps(create(Path(args.create)), indent=2)); return 0
    if not args.briefing: ap.error("use --create or --briefing")
    print(json.dumps(review(Path(args.briefing), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
