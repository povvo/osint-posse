#!/usr/bin/env python3
"""Quantitative Social Network Analysis (SNA).

Calculates degree, density, component size, reciprocity, and simple bridge-node
indicators from a directed edge CSV.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter, defaultdict, deque
from pathlib import Path


def edges_from_csv(path: Path, source_col: str, target_col: str) -> list[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [(r[source_col].strip(), r[target_col].strip()) for r in csv.DictReader(handle) if r.get(source_col) and r.get(target_col)]


def components(nodes: set[str], edges: list[tuple[str, str]]) -> list[set[str]]:
    adj: dict[str, set[str]] = defaultdict(set)
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    seen, out = set(), []
    for node in nodes:
        if node in seen: continue
        q, comp = deque([node]), set([node])
        seen.add(node)
        while q:
            cur = q.popleft()
            for nxt in adj[cur]:
                if nxt not in seen:
                    seen.add(nxt); comp.add(nxt); q.append(nxt)
        out.append(comp)
    return out


def analyse(edges: list[tuple[str, str]]) -> dict:
    nodes = {n for edge in edges for n in edge}
    out_d, in_d = Counter(), Counter()
    directed = set(edges)
    for a, b in edges:
        out_d[a] += 1; in_d[b] += 1
    node_rows = []
    for n in sorted(nodes):
        node_rows.append({"node": n, "in_degree": in_d[n], "out_degree": out_d[n], "total_degree": in_d[n] + out_d[n], "possible_bridge": in_d[n] > 0 and out_d[n] > 0})
    max_edges = len(nodes) * (len(nodes) - 1) if len(nodes) > 1 else 0
    reciprocal = {tuple(sorted((a, b))) for a, b in directed if a != b and (b, a) in directed}
    comps = components(nodes, edges)
    return {"node_count": len(nodes), "edge_count": len(edges), "density": (len(directed) / max_edges) if max_edges else 0, "reciprocal_pairs": len(reciprocal), "component_count": len(comps), "largest_component": max((len(c) for c in comps), default=0), "nodes": sorted(node_rows, key=lambda r: (-r["total_degree"], r["node"]))}


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute social-network metrics from an edge CSV.")
    ap.add_argument("edge_csv"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target"); ap.add_argument("--output")
    args = ap.parse_args()
    result = analyse(edges_from_csv(Path(args.edge_csv), args.source_col, args.target_col))
    if args.output: Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
