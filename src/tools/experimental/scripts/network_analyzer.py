#!/usr/bin/env python3
"""network_analyzer.py.

Analyses a directed edge CSV with standard-library graph metrics: degree,
weak components, self-loops, reciprocal edges, and GraphML export.
"""
from __future__ import annotations
import argparse, csv, json, xml.sax.saxutils as sx
from collections import Counter, defaultdict, deque
from pathlib import Path


def read_edges(path: Path, source_col: str, target_col: str) -> list[tuple[str, str, dict]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    edges = []
    for row in rows:
        source, target = str(row.get(source_col, "")).strip(), str(row.get(target_col, "")).strip()
        if source and target: edges.append((source, target, row))
    return edges


def analyse(edges: list[tuple[str, str, dict]]) -> dict:
    nodes = sorted({n for s, t, _ in edges for n in (s, t)})
    out_degree, in_degree = Counter(), Counter(); adjacency: dict[str, set[str]] = defaultdict(set)
    directed = set(); reciprocal = set(); self_loops = []
    for source, target, _ in edges:
        out_degree[source] += 1; in_degree[target] += 1; adjacency[source].add(target); adjacency[target].add(source); directed.add((source, target))
        if source == target: self_loops.append(source)
    for source, target in directed:
        if source != target and (target, source) in directed: reciprocal.add(tuple(sorted((source, target))))
    seen, components = set(), []
    for node in nodes:
        if node in seen: continue
        queue, comp = deque([node]), []
        seen.add(node)
        while queue:
            cur = queue.popleft(); comp.append(cur)
            for nxt in adjacency[cur]:
                if nxt not in seen: seen.add(nxt); queue.append(nxt)
        components.append(sorted(comp))
    metrics = [{"node": n, "in_degree": in_degree[n], "out_degree": out_degree[n], "total_degree": in_degree[n] + out_degree[n]} for n in nodes]
    metrics.sort(key=lambda x: (-x["total_degree"], x["node"]))
    return {"node_count": len(nodes), "edge_count": len(edges), "component_count": len(components), "self_loops": self_loops, "reciprocal_edge_pairs": len(reciprocal), "top_nodes": metrics[:50], "components": [{"size": len(c), "nodes": c} for c in sorted(components, key=len, reverse=True)]}


def write_graphml(edges: list[tuple[str, str, dict]], path: Path) -> None:
    nodes = sorted({n for s, t, _ in edges for n in (s, t)})
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">', '<graph edgedefault="directed">']
    for node in nodes: lines.append(f'<node id="{sx.escape(node)}"/>')
    for i, (source, target, _) in enumerate(edges): lines.append(f'<edge id="e{i}" source="{sx.escape(source)}" target="{sx.escape(target)}"/>')
    lines += ["</graph>", "</graphml>"]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyse a directed edge list CSV.")
    ap.add_argument("edge_csv"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target")
    ap.add_argument("--json-output"); ap.add_argument("--graphml-output")
    args = ap.parse_args()
    edges = read_edges(Path(args.edge_csv), args.source_col, args.target_col)
    result = analyse(edges)
    if args.json_output: Path(args.json_output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.graphml_output: write_graphml(edges, Path(args.graphml_output))
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
