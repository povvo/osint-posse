#!/usr/bin/env python3
"""Neo4j / Cypher workbench.

Converts node and edge CSV files into Cypher import statements and validates
required graph columns before loading into any external system.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

SAFE_LABEL = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,60}$")


def q(value: str) -> str:
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def label(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip())
    if not cleaned or not cleaned[0].isalpha(): cleaned = "Node"
    return cleaned[:60]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def node_statement(row: dict, node_label: str, id_col: str) -> str:
    props = ", ".join(f"{re.sub(r'[^A-Za-z0-9_]+','_',k)}: {q(v)}" for k, v in row.items() if v not in (None, ""))
    return f"MERGE (n:{label(node_label)} {{id: {q(row[id_col])}}}) SET n += {{{props}}};"


def edge_statement(row: dict, src: str, dst: str, rel_type: str) -> str:
    rel = label(row.get(rel_type, "RELATED_TO")).upper()
    return f"MATCH (a {{id: {q(row[src])}}}), (b {{id: {q(row[dst])}}}) MERGE (a)-[:{rel}]->(b);"


def build(nodes_csv: Path, edges_csv: Path, output: Path, id_col: str, source_col: str, target_col: str, rel_col: str, node_label: str) -> dict:
    nodes = read_csv(nodes_csv); edges = read_csv(edges_csv)
    missing = []
    for i, row in enumerate(nodes, 1):
        if not row.get(id_col): missing.append({"file": str(nodes_csv), "row": i, "missing": id_col})
    for i, row in enumerate(edges, 1):
        for col in (source_col, target_col):
            if not row.get(col): missing.append({"file": str(edges_csv), "row": i, "missing": col})
    lines = ["// Generated Cypher import script"]
    if not missing:
        lines += [node_statement(row, node_label, id_col) for row in nodes]
        lines += [edge_statement(row, source_col, target_col, rel_col) for row in edges]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"nodes": len(nodes), "edges": len(edges), "cypher": str(output), "findings": missing, "ok": not missing}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create Cypher MERGE statements from node and edge CSV files.")
    ap.add_argument("--nodes", required=True); ap.add_argument("--edges", required=True); ap.add_argument("--output", default="import.cypher")
    ap.add_argument("--id-col", default="id"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target"); ap.add_argument("--rel-col", default="relationship"); ap.add_argument("--label", default="Entity")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.nodes), Path(args.edges), Path(args.output), args.id_col, args.source_col, args.target_col, args.rel_col, args.label), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
