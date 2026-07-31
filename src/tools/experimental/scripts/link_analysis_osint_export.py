#!/usr/bin/env python3
"""Maltego-style link analysis / OSINT export.

Normalises public-research entities and relationships into importable node and
edge CSVs for link-analysis tools.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def clean_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", value.strip())[:120]


def export(input_csv: Path, output_dir: Path, entity_col: str, type_col: str, source_col: str, target_col: str) -> dict:
    rows = read(input_csv); nodes = {}; edges = []
    for row in rows:
        entity = clean_id(row.get(entity_col, ""))
        if entity: nodes.setdefault(entity, {"id": entity, "label": row.get(entity_col, ""), "type": row.get(type_col, "Entity")})
        src, dst = clean_id(row.get(source_col, "")), clean_id(row.get(target_col, ""))
        if src and dst: edges.append({"source": src, "target": dst, "relationship": row.get("relationship", "related_to"), "source_ref": row.get("source_ref", "")})
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "label", "type"]); writer.writeheader(); writer.writerows(nodes.values())
    with (output_dir / "edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "relationship", "source_ref"]); writer.writeheader(); writer.writerows(edges)
    return {"nodes": len(nodes), "edges": len(edges), "output_dir": str(output_dir)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Export entity/link CSVs for link-analysis review.")
    ap.add_argument("input_csv"); ap.add_argument("--entity-col", default="entity"); ap.add_argument("--type-col", default="type"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target"); ap.add_argument("--output-dir", default="link_analysis_export")
    args = ap.parse_args()
    print(json.dumps(export(Path(args.input_csv), Path(args.output_dir), args.entity_col, args.type_col, args.source_col, args.target_col), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
