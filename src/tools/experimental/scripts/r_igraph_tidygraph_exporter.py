#!/usr/bin/env python3
"""R igraph / tidygraph exporter.

Exports edge and node CSV files plus an R script scaffold for igraph/tidygraph
analysis without requiring R to be installed.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def export(edge_csv: Path, output_dir: Path, source_col: str, target_col: str) -> dict:
    edges = [r for r in read(edge_csv) if r.get(source_col) and r.get(target_col)]
    nodes = sorted({r[source_col] for r in edges} | {r[target_col] for r in edges})
    output_dir.mkdir(parents=True, exist_ok=True)
    nodes_path, edges_path, script_path = output_dir / "nodes.csv", output_dir / "edges.csv", output_dir / "igraph_analysis.R"
    with nodes_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name"]); writer.writeheader(); writer.writerows([{"name": n} for n in nodes])
    with edges_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["from", "to"]); writer.writeheader(); writer.writerows([{"from": r[source_col], "to": r[target_col]} for r in edges])
    script_path.write_text("library(igraph)\nedges <- read.csv('edges.csv')\ng <- graph_from_data_frame(edges, directed=TRUE)\nprint(summary(g))\nprint(degree(g))\n", encoding="utf-8")
    return {"output_dir": str(output_dir), "nodes": len(nodes), "edges": len(edges), "r_script": str(script_path)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create igraph/tidygraph import files and R scaffold.")
    ap.add_argument("edge_csv"); ap.add_argument("--output-dir", default="r_graph_export"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target")
    args = ap.parse_args()
    print(json.dumps(export(Path(args.edge_csv), Path(args.output_dir), args.source_col, args.target_col), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
