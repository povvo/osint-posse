#!/usr/bin/env python3
"""Claims-to-sources audit sheet.

Extracts claim rows from CSV/JSON and creates an audit sheet that requires a
source reference, confidence, and reviewer decision for each claim.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = ["claim_id", "claim", "source_ref", "confidence", "review_decision", "reviewer", "notes"]


def read(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(rows: list[dict], output: Path) -> dict:
    out = []
    warnings = []
    for i, row in enumerate(rows, 1):
        claim = row.get("claim") or row.get("finding") or row.get("text") or row.get("note") or ""
        source = row.get("source_ref") or row.get("source") or ""
        confidence = row.get("confidence") or ""
        if claim and not source: warnings.append({"claim_id": f"C{i:03d}", "issue": "missing source"})
        out.append({"claim_id": f"C{i:03d}", "claim": claim, "source_ref": source, "confidence": confidence, "review_decision": "pending", "reviewer": "", "notes": ""})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(out)
    return {"output": str(output), "claims": len(out), "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a claims-to-sources audit sheet.")
    ap.add_argument("input"); ap.add_argument("--output", default="claims_to_sources_audit.csv")
    args = ap.parse_args()
    print(json.dumps(build(read(Path(args.input)), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
