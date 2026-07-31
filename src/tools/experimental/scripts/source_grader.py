#!/usr/bin/env python3
"""source_grader.py.

Grades source reliability and information credibility using the Admiralty 6x6
model and emits structured JSON or CSV-ready records.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone

RELIABILITY = {"A": "completely reliable", "B": "usually reliable", "C": "fairly reliable", "D": "not usually reliable", "E": "unreliable", "F": "cannot judge"}
CREDIBILITY = {"1": "confirmed", "2": "probably true", "3": "possibly true", "4": "doubtful", "5": "improbable", "6": "cannot judge"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def recommendation(rel: str, cred: str) -> str:
    score = (ord(rel) - ord("A")) + (int(cred) - 1)
    if score <= 2: return "use_with_high_confidence"
    if score <= 4: return "use_with_caveat"
    if score <= 6: return "corroborate_before_synthesis"
    return "do_not_use_without_review"


def grade(source: str, claim: str, reliability: str, credibility: str, rationale: str) -> dict:
    reliability = reliability.upper(); credibility = str(credibility)
    if reliability not in RELIABILITY: raise ValueError("reliability must be A-F")
    if credibility not in CREDIBILITY: raise ValueError("credibility must be 1-6")
    return {"graded_utc": now(), "source": source, "claim": claim, "reliability": reliability, "reliability_label": RELIABILITY[reliability], "credibility": credibility, "credibility_label": CREDIBILITY[credibility], "combined": reliability + credibility, "recommendation": recommendation(reliability, credibility), "rationale": rationale}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an Admiralty 6x6 source grade.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--claim", required=True)
    parser.add_argument("--reliability", required=True, choices=sorted(RELIABILITY))
    parser.add_argument("--credibility", required=True, choices=sorted(CREDIBILITY))
    parser.add_argument("--rationale", default="")
    args = parser.parse_args()
    print(json.dumps(grade(args.source, args.claim, args.reliability, args.credibility, args.rationale), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
