#!/usr/bin/env python3
"""Style guide / analytic tradecraft checklist.

Checks a report for common tradecraft issues: unsourced claims, vague confidence,
missing caveats, and mixed fact/judgement language.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

CLAIM = re.compile(r"\b(is|are|was|were|shows|confirms|proves|indicates|suggests)\b", re.I)
SOURCE = re.compile(r"\[[^\]]+\]|source[: ]", re.I)
VAGUE = re.compile(r"\b(maybe|sort of|kind of|seems|feels|clearly|obviously)\b", re.I)


def check(path: Path, output: Path) -> dict:
    rows = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_no, line in enumerate(text.splitlines(), 1):
        issues = []
        if CLAIM.search(line) and not SOURCE.search(line): issues.append("claim-like line lacks source marker")
        if VAGUE.search(line): issues.append("vague or loaded wording")
        if "## Caveats" not in text and line_no == 1: issues.append("document may lack Caveats section")
        if issues: rows.append({"line": line_no, "issues": "; ".join(issues), "text": line.strip()})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["line", "issues", "text"]); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "issues": len(rows), "ok": not rows}


def main() -> int:
    ap = argparse.ArgumentParser(description="Run an analytic tradecraft checklist on a text report.")
    ap.add_argument("report"); ap.add_argument("--output", default="tradecraft_review.csv")
    args = ap.parse_args()
    print(json.dumps(check(Path(args.report), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
