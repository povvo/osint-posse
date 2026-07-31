#!/usr/bin/env python3
"""Dissemination readiness checklist.

Validates a product before release for required sections, source summary, caveats,
handling restrictions, versioning, and recipient entry.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

CHECKS = ["bottom_line", "source_summary", "confidence", "caveats", "handling", "version", "recipient"]
PATTERNS = {"bottom_line": r"BLUF|Bottom Line", "source_summary": r"Source Summary|Sources", "confidence": r"Confidence|likely|unlikely|high|medium|low", "caveats": r"Caveat|Limitation", "handling": r"Handling|Restriction", "version": r"Version", "recipient": r"Recipient|Audience"}


def review(product: Path, output: Path) -> dict:
    text = product.read_text(encoding="utf-8", errors="replace")
    rows = []
    for check in CHECKS:
        ok = bool(re.search(PATTERNS[check], text, re.I))
        rows.append({"check": check, "status": "pass" if ok else "review", "notes": ""})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "notes"]); writer.writeheader(); writer.writerows(rows)
    return {"output": str(output), "ready": all(r["status"] == "pass" for r in rows), "review_items": sum(1 for r in rows if r["status"] == "review")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Check dissemination readiness for a report or briefing.")
    ap.add_argument("product"); ap.add_argument("--output", default="dissemination_readiness.csv")
    args = ap.parse_args()
    print(json.dumps(review(Path(args.product), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
