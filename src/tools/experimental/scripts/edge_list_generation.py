#!/usr/bin/env python3
"""Edge List Generation.

Extracts directed edges from tabular data by selecting source, target, relation,
and source-reference columns. Produces a normalised edge CSV and validation report.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path

FIELDS = ["source", "target", "relationship", "source_ref", "confidence", "notes"]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_edges(rows: list[dict], source_col: str, target_col: str, rel_col: str | None, ref_col: str | None, default_rel: str) -> tuple[list[dict], list[dict]]:
    edges, findings = [], []
    for idx, row in enumerate(rows, 1):
        src, dst = str(row.get(source_col, "")).strip(), str(row.get(target_col, "")).strip()
        if not src or not dst:
            findings.append({"row": idx, "issue": "missing source or target"}); continue
        relation = str(row.get(rel_col, "")).strip() if rel_col else default_rel
        source_ref = str(row.get(ref_col, "")).strip() if ref_col else ""
        edges.append({"source": src, "target": dst, "relationship": relation or default_rel, "source_ref": source_ref, "confidence": "low", "notes": ""})
    return edges, findings


def write_edges(path: Path, edges: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(edges)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a normalised graph edge list from CSV.")
    ap.add_argument("input_csv"); ap.add_argument("--source-col", required=True); ap.add_argument("--target-col", required=True)
    ap.add_argument("--relationship-col"); ap.add_argument("--source-ref-col"); ap.add_argument("--default-relationship", default="related_to")
    ap.add_argument("--output", default="edges.csv")
    args = ap.parse_args()
    rows = read_csv(Path(args.input_csv))
    edges, findings = build_edges(rows, args.source_col, args.target_col, args.relationship_col, args.source_ref_col, args.default_relationship)
    write_edges(Path(args.output), edges)
    report = {"input_rows": len(rows), "edges": len(edges), "output": args.output, "findings": findings, "duplicate_edges": sum(c - 1 for c in Counter((e['source'], e['target'], e['relationship']) for e in edges).values() if c > 1)}
    print(json.dumps(report, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
