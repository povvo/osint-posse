#!/usr/bin/env python3
"""Issuing the Findings Memo.

Validates a findings memo before issue, checking required headings, source
markers, confidence wording, and dissemination details.
"""
from __future__ import annotations
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = ["Purpose", "Key Findings", "Evidence Summary", "Confidence", "Caveats", "Recommended Actions"]
SOURCE_MARKER = re.compile(r"\[[^\]]+\]|source[: ]", re.I)
CONFIDENCE = re.compile(r"\b(low|medium|high|likely|unlikely|almost certain|roughly even)\b", re.I)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate(memo: Path, recipient: str, output: Path) -> dict:
    text = memo.read_text(encoding="utf-8", errors="replace")
    findings = []
    for heading in REQUIRED:
        if f"## {heading}" not in text: findings.append({"issue": "missing heading", "heading": heading})
    if not SOURCE_MARKER.search(text): findings.append({"issue": "no source marker found"})
    if not CONFIDENCE.search(text): findings.append({"issue": "no confidence wording found"})
    record = {"memo": str(memo), "recipient": recipient, "reviewed_utc": now(), "ready_to_issue": not findings, "findings": findings}
    output.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a findings memo before issue.")
    ap.add_argument("memo"); ap.add_argument("--recipient", required=True); ap.add_argument("--output", default="findings_memo_issue_check.json")
    args = ap.parse_args()
    print(json.dumps(validate(Path(args.memo), args.recipient, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
