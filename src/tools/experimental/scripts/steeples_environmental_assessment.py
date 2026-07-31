#!/usr/bin/env python3
"""Environmental Assessment (STEEPLES).

Creates a STEEPLES assessment matrix covering social, technological, economic,
environmental, political, legal, ethical, and security factors.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FACTORS = ["social", "technological", "economic", "environmental", "political", "legal", "ethical", "security"]


def create(output: Path, topic: str) -> dict:
    fields = ["factor", "topic", "observation", "source_ref", "impact", "likelihood", "confidence", "gap", "action"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for factor in FACTORS:
            writer.writerow({"factor": factor, "topic": topic, "observation": "", "source_ref": "", "impact": "", "likelihood": "", "confidence": "", "gap": "", "action": ""})
    return {"output": str(output), "topic": topic, "factors": FACTORS}


def summarise(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    gaps = [row for row in rows if row.get("gap")]
    actions = [row for row in rows if row.get("action")]
    return {"rows": len(rows), "gaps": len(gaps), "actions": len(actions), "factors": sorted({row.get("factor", "") for row in rows})}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or summarise a STEEPLES assessment matrix.")
    parser.add_argument("--create")
    parser.add_argument("--topic", default="assessment topic")
    parser.add_argument("--summarise")
    args = parser.parse_args()
    if args.create:
        print(json.dumps(create(Path(args.create), args.topic), indent=2)); return 0
    if not args.summarise:
        parser.error("use --create or --summarise")
    print(json.dumps(summarise(Path(args.summarise)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
