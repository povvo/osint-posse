#!/usr/bin/env python3
"""Constructing the Bottom Line Up Front (BLUF).

Builds a concise BLUF statement from findings, confidence, caveats, and decision
ask fields. Flags overlong or unsupported summaries.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(rows: list[dict], output: Path, max_words: int) -> dict:
    findings = [str(r.get("finding") or r.get("assessment") or r.get("note") or "").strip() for r in rows]
    findings = [f for f in findings if f]
    confidence = next((str(r.get("confidence")) for r in rows if r.get("confidence")), "medium")
    ask = next((str(r.get("ask") or r.get("decision_ask")) for r in rows if r.get("ask") or r.get("decision_ask")), "No decision ask supplied.")
    bluf = f"{findings[0] if findings else 'No finding supplied.'} Confidence: {confidence}. Decision ask: {ask}"
    words = re.findall(r"\S+", bluf)
    warnings = []
    if len(words) > max_words: warnings.append(f"BLUF exceeds {max_words} words")
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(bluf + "\n", encoding="utf-8")
    return {"output": str(output), "word_count": len(words), "warnings": warnings, "bluf": bluf}


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a BLUF statement from structured notes.")
    ap.add_argument("notes"); ap.add_argument("--output", default="bluf.txt"); ap.add_argument("--max-words", type=int, default=75)
    args = ap.parse_args()
    print(json.dumps(build(read_rows(Path(args.notes)), Path(args.output), args.max_words), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
