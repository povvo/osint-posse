#!/usr/bin/env python3
"""Red-team / devil's advocate checklist.

Creates and applies a structured challenge checklist to stress-test dominant
explanations, evidence gaps, and analytic confidence.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

QUESTIONS = [
    "What evidence would disprove the leading explanation?",
    "What alternative explanation fits the same facts?",
    "Which source could be biased, mistaken, or incomplete?",
    "What collection gap most affects the conclusion?",
    "What assumption is carrying the most weight?",
    "What would change the confidence level?",
]


def create(output: Path) -> dict:
    rows = [{"question_id": f"Q{i+1}", "question": q, "answer": "", "action": "", "owner": ""} for i, q in enumerate(QUESTIONS)]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["question_id", "question", "answer", "action", "owner"])
        writer.writeheader(); writer.writerows(rows)
    return {"created": str(output), "questions": len(rows)}


def audit(input_csv: Path) -> dict:
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    unanswered = [row.get("question_id") for row in rows if not row.get("answer")]
    open_actions = [row.get("question_id") for row in rows if row.get("action") and not row.get("owner")]
    return {"questions": len(rows), "unanswered": unanswered, "actions_without_owner": open_actions, "complete": not unanswered and not open_actions}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or audit a red-team checklist.")
    parser.add_argument("--create")
    parser.add_argument("--audit")
    args = parser.parse_args()
    if args.create: print(json.dumps(create(Path(args.create)), indent=2)); return 0
    if not args.audit: parser.error("use --create or --audit")
    print(json.dumps(audit(Path(args.audit)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
