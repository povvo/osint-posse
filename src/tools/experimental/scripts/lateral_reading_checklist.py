#!/usr/bin/env python3
"""Lateral-reading checklist.

Creates a source comparison checklist that distinguishes original reporting,
repeated claims, independent corroboration, and circular citation.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path

FIELDS = ["claim", "source", "publisher", "publication_date", "original_or_repeat", "independent", "notes"]


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def analyse(rows: list[dict]) -> dict:
    by_claim: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_claim[str(row.get("claim", "")).strip().lower()].append(row)
    findings = []
    for claim, items in by_claim.items():
        publishers = {str(i.get("publisher", "")).strip().lower() for i in items if i.get("publisher")}
        originals = [i for i in items if str(i.get("original_or_repeat", "")).lower() == "original"]
        findings.append({"claim": claim, "source_count": len(items), "publisher_count": len(publishers), "has_original": bool(originals), "independent_enough": len(publishers) >= 2 and bool(originals)})
    return {"claims": len(findings), "findings": findings}


def init(output: Path) -> dict:
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader()
    return {"created": str(output), "fields": FIELDS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or analyse a lateral-reading checklist.")
    parser.add_argument("--init")
    parser.add_argument("--input")
    parser.add_argument("--output", default="lateral_reading_report.json")
    args = parser.parse_args()
    if args.init:
        print(json.dumps(init(Path(args.init)), indent=2)); return 0
    if not args.input: parser.error("use --init or --input")
    report = analyse(read(Path(args.input)))
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "claims": report["claims"]}, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
