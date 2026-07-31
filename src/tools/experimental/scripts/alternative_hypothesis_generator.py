#!/usr/bin/env python3
"""Alternative hypothesis generator.

Builds competing-explanation prompts from a leading hypothesis, evidence gaps,
and possible error, deception, coincidence, and misclassification paths.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

FRAMES = [
    "The observed facts are accurate, but the causal explanation is different.",
    "One or more key observations are mistaken or misclassified.",
    "The pattern is produced by coincidence, base-rate effects, or selection bias.",
    "A missing actor, event, or source changes the explanation.",
    "The leading hypothesis relies on an untested assumption.",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def generate(leading: str, output: Path, gap: list[str]) -> dict:
    rows = []
    for idx, frame in enumerate(FRAMES, 1):
        rows.append({"hypothesis_id": f"ALT{idx}", "alternative": f"Alternative to '{leading}': {frame}", "evidence_needed": gap[idx-1] if idx <= len(gap) else "Identify evidence that would distinguish this alternative.", "created_utc": now()})
    output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return {"output": str(output), "alternatives": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate alternative hypotheses for structured challenge.")
    parser.add_argument("--leading", required=True)
    parser.add_argument("--gap", action="append", default=[])
    parser.add_argument("--output", default="alternative_hypotheses.json")
    args = parser.parse_args()
    print(json.dumps(generate(args.leading, Path(args.output), args.gap), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
