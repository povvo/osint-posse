#!/usr/bin/env python3
"""Association matrix.

Builds a square entity association matrix from an edge CSV, preserving direct,
indirect, and uncertain relationship labels as cell values.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(edge_csv: Path, output: Path, source_col: str, target_col: str, rel_col: str) -> dict:
    rows = read(edge_csv)
    entities = sorted({r[source_col] for r in rows if r.get(source_col)} | {r[target_col] for r in rows if r.get(target_col)})
    matrix = {a: {b: "" for b in entities} for a in entities}
    for row in rows:
        a, b = row.get(source_col, ""), row.get(target_col, "")
        if a and b:
            rel = row.get(rel_col, "related") or "related"
            matrix[a][b] = rel if not matrix[a][b] else matrix[a][b] + ";" + rel
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle); writer.writerow(["entity", *entities])
        for entity in entities: writer.writerow([entity, *[matrix[entity][other] for other in entities]])
    return {"output": str(output), "entities": len(entities), "edges": len(rows)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create an association matrix from an edge CSV.")
    ap.add_argument("edge_csv"); ap.add_argument("--output", default="association_matrix.csv"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target"); ap.add_argument("--relationship-col", default="relationship")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.edge_csv), Path(args.output), args.source_col, args.target_col, args.relationship_col), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
