#!/usr/bin/env python3
"""Civil/parish/probate source checklist.

Creates a systematic source-class checklist for civil, parish, probate, migration,
and related record searches.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

ROWS = [
    ("civil_birth", "Civil birth registration"),
    ("civil_marriage", "Civil marriage registration"),
    ("civil_death", "Civil death registration"),
    ("parish_baptism", "Parish baptism record"),
    ("parish_marriage", "Parish marriage record"),
    ("parish_burial", "Parish burial record"),
    ("probate", "Will, probate, or administration record"),
    ("census", "Census or household schedule"),
    ("migration", "Passenger, immigration, or naturalisation record"),
]


def create(output: Path, person: str) -> dict:
    fields = ["record_class", "description", "person_or_family", "repository", "searched", "result", "citation", "conflict_note"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record_class, description in ROWS:
            writer.writerow({"record_class": record_class, "description": description, "person_or_family": person, "repository": "", "searched": "no", "result": "", "citation": "", "conflict_note": ""})
    return {"output": str(output), "rows": len(ROWS)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create civil/parish/probate source checklist.")
    parser.add_argument("--person", required=True)
    parser.add_argument("--output", default="civil_parish_probate_checklist.csv")
    args = parser.parse_args()
    print(json.dumps(create(Path(args.output), args.person), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
