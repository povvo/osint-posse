#!/usr/bin/env python3
"""Genealogy proof/citation template.

Creates a proof argument worksheet with claim, evidence items, conflicting
records, reasoning, citation standard, and conclusion status.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["proof_id", "research_question", "claim", "evidence_summary", "conflicting_evidence", "reasoning", "citation", "conclusion", "status", "reviewer"]


def create(output: Path) -> dict:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
    md = output.with_suffix(".md")
    md.write_text("# Genealogy Proof Worksheet\n\nUse the CSV to document proof arguments, conflicts, citations, and conclusion status.\n", encoding="utf-8")
    return {"csv": str(output), "markdown": str(md), "fields": FIELDS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a genealogy proof/citation worksheet.")
    parser.add_argument("--output", default="genealogy_proof.csv")
    args = parser.parse_args()
    print(json.dumps(create(Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
