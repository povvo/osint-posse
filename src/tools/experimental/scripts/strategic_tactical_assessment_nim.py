#!/usr/bin/env python3
"""Strategic and Tactical Assessments (NIM).

Converts structured issue rows into strategic/tactical assessment sections and
prioritised intelligence requirements.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def score(row: dict) -> int:
    return int(row.get("impact", 1) or 1) * int(row.get("likelihood", 1) or 1)


def build(rows: list[dict], output: Path) -> dict:
    ranked = sorted(rows, key=score, reverse=True)
    lines = ["# NIM Strategic and Tactical Assessment", "", "## Strategic Overview", ""]
    for row in ranked[:5]: lines.append(f"- {row.get('issue','Issue')} · score {score(row)}")
    lines += ["", "## Tactical Requirements", ""]
    for row in ranked: lines.append(f"- Requirement: {row.get('requirement') or row.get('gap') or row.get('issue','')} · Owner: {row.get('owner','')}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"output": str(output), "issues": len(rows), "top_score": score(ranked[0]) if ranked else 0, "by_owner": dict(Counter(r.get("owner", "unassigned") for r in rows))}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a NIM-style strategic/tactical assessment from CSV rows.")
    ap.add_argument("issues_csv"); ap.add_argument("--output", default="nim_assessment.md")
    args = ap.parse_args()
    print(json.dumps(build(read(Path(args.issues_csv)), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
