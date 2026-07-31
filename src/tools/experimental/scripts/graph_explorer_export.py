#!/usr/bin/env python3
"""Neo4j Bloom / graph explorer.

Creates graph-explorer perspective files: node categories, relationship labels,
and suggested search phrases from existing node and edge CSVs.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(nodes_csv: Path, edges_csv: Path, output: Path) -> dict:
    nodes, edges = read(nodes_csv), read(edges_csv)
    types = Counter(row.get("type", "Entity") or "Entity" for row in nodes)
    rels = Counter(row.get("relationship", "RELATED_TO") or "RELATED_TO" for row in edges)
    perspective = {
        "node_categories": [{"label": k, "count": v, "caption": "label"} for k, v in types.items()],
        "relationship_categories": [{"type": k, "count": v} for k, v in rels.items()],
        "search_phrases": ["Find entity by name", "Show neighbours", "Expand relationship path", "Filter by source reference"],
    }
    output.write_text(json.dumps(perspective, indent=2), encoding="utf-8")
    return {"output": str(output), "node_types": len(types), "relationship_types": len(rels)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a graph-explorer perspective JSON file.")
    ap.add_argument("--nodes", required=True); ap.add_argument("--edges", required=True); ap.add_argument("--output", default="graph_explorer_perspective.json")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.nodes), Path(args.edges), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
