#!/usr/bin/env python3
"""Quantitative Analysis and Drawing Conclusions.

Converts ACH scores into ranked conclusions, margin notes, and a confidence flag
based on the distance between the strongest hypotheses.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def conclude(summary_json: Path, output: Path) -> dict:
    data = json.loads(summary_json.read_text(encoding="utf-8"))
    hypotheses = sorted(data.get("hypotheses", []), key=lambda row: row.get("total", 0), reverse=True)
    if not hypotheses:
        result = {"conclusion": "no hypotheses scored", "confidence_flag": "none", "ranking": []}
    else:
        top = hypotheses[0]
        runner_up = hypotheses[1] if len(hypotheses) > 1 else None
        margin = top.get("total", 0) - (runner_up.get("total", 0) if runner_up else 0)
        confidence = "strong" if margin >= 5 else "moderate" if margin >= 2 else "weak"
        result = {"conclusion": f"Leading hypothesis: {top.get('hypothesis')}", "confidence_flag": confidence, "margin": margin, "ranking": hypotheses}
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return {"output": str(output), "confidence_flag": result["confidence_flag"], "conclusion": result["conclusion"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank ACH hypotheses and draw a conclusion note.")
    parser.add_argument("summary_json")
    parser.add_argument("--output", default="ach_conclusion.json")
    args = parser.parse_args()
    print(json.dumps(conclude(Path(args.summary_json), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
