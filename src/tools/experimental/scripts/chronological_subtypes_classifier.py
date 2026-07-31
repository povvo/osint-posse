#!/usr/bin/env python3
"""Chronological Sub-Types.

Classifies chronology rows into event subtypes such as observation, communication,
transaction, movement, publication, custody, and decision.
"""
from __future__ import annotations
import argparse, csv, json, re
from collections import Counter
from pathlib import Path

RULES = {
    "communication": re.compile(r"\b(email|call|message|letter|meeting|interview)\b", re.I),
    "transaction": re.compile(r"\b(payment|transfer|invoice|purchase|transaction|ledger)\b", re.I),
    "movement": re.compile(r"\b(travel|arrive|depart|location|journey|visit)\b", re.I),
    "publication": re.compile(r"\b(published|posted|article|report|notice|filing)\b", re.I),
    "custody": re.compile(r"\b(received|stored|sealed|released|custody|evidence)\b", re.I),
    "decision": re.compile(r"\b(decided|approved|rejected|authorised|tasked)\b", re.I),
}


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def classify(text: str) -> str:
    for label, regex in RULES.items():
        if regex.search(text):
            return label
    return "observation"


def process(input_csv: Path, output_csv: Path) -> dict:
    rows = read_rows(input_csv)
    for row in rows:
        text = " ".join(str(value) for value in row.values() if value)
        row["chronology_subtype"] = classify(text)
    fields = sorted({key for row in rows for key in row}) if rows else ["chronology_subtype"]
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    return {"output": str(output_csv), "rows": len(rows), "counts": dict(Counter(row["chronology_subtype"] for row in rows))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify chronology entries by event subtype.")
    parser.add_argument("input_csv")
    parser.add_argument("--output", default="chronology_subtypes.csv")
    args = parser.parse_args()
    print(json.dumps(process(Path(args.input_csv), Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
