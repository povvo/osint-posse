#!/usr/bin/env python3
"""Hypothesis Generation and Matrix Setup.

Creates a hypothesis register and expands it against evidence rows to initialise
an ACH-style scoring matrix.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def setup(evidence_csv: Path, hypotheses: list[str], output_dir: Path) -> dict:
    evidence = read(evidence_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    hyp_rows = [{"hypothesis_id": f"H{i+1}", "hypothesis": text, "status": "active"} for i, text in enumerate(hypotheses)]
    matrix = []
    for e_idx, row in enumerate(evidence, 1):
        evidence_id = row.get("evidence_id") or f"E{e_idx:04d}"
        evidence_text = row.get("evidence") or row.get("claim") or row.get("finding") or row.get("note") or ""
        for hyp in hyp_rows:
            matrix.append({"evidence_id": evidence_id, "evidence": evidence_text, "hypothesis_id": hyp["hypothesis_id"], "hypothesis": hyp["hypothesis"], "score": "unscored", "diagnosticity": "", "notes": ""})
    write(output_dir / "hypotheses.csv", hyp_rows, ["hypothesis_id", "hypothesis", "status"])
    write(output_dir / "ach_matrix.csv", matrix, ["evidence_id", "evidence", "hypothesis_id", "hypothesis", "score", "diagnosticity", "notes"])
    return {"output_dir": str(output_dir), "hypotheses": len(hyp_rows), "matrix_rows": len(matrix)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialise hypotheses and ACH matrix rows.")
    parser.add_argument("evidence_csv")
    parser.add_argument("--hypothesis", action="append", required=True)
    parser.add_argument("--output-dir", default="hypothesis_matrix")
    args = parser.parse_args()
    print(json.dumps(setup(Path(args.evidence_csv), args.hypothesis, Path(args.output_dir)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
