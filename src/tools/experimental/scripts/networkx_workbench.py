#!/usr/bin/env python3
"""NetworkX workbench.

Runs graph analysis with NetworkX when installed, otherwise uses a standard-library
fallback for degree and component metrics. Accepts source/target edge CSVs.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter, defaultdict, deque
from pathlib import Path


def read_edges(path: Path, source_col: str, target_col: str) -> list[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [(r[source_col].strip(), r[target_col].strip()) for r in csv.DictReader(handle) if r.get(source_col) and r.get(target_col)]


def fallback(edges: list[tuple[str, str]]) -> dict:
    nodes = sorted({n for e in edges for n in e})
    deg = Counter(); adj: dict[str, set[str]] = defaultdict(set)
    for a, b in edges:
        deg[a] += 1; deg[b] += 1; adj[a].add(b); adj[b].add(a)
    seen, comps = set(), []
    for node in nodes:
        if node in seen: continue
        queue, comp = deque([node]), []
        seen.add(node)
        while queue:
            item = queue.popleft(); comp.append(item)
            for nxt in adj[item]:
                if nxt not in seen: seen.add(nxt); queue.append(nxt)
        comps.append(comp)
    return {"engine": "standard_library", "nodes": len(nodes), "edges": len(edges), "components": len(comps), "top_degree": deg.most_common(25)}


def with_networkx(edges: list[tuple[str, str]]) -> dict:
    import networkx as nx  # type: ignore
    graph = nx.DiGraph(); graph.add_edges_from(edges)
    undirected = graph.to_undirected()
    centrality = nx.degree_centrality(graph)
    return {"engine": "networkx", "nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(), "weak_components": nx.number_weakly_connected_components(graph), "density": nx.density(graph), "top_degree_centrality": sorted(centrality.items(), key=lambda kv: kv[1], reverse=True)[:25], "connected_components": [sorted(c) for c in nx.connected_components(undirected)]}


def analyse(path: Path, source_col: str, target_col: str, require_networkx: bool) -> dict:
    edges = read_edges(path, source_col, target_col)
    try:
        return with_networkx(edges)
    except ImportError:
        if require_networkx: raise
        return fallback(edges)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run NetworkX-compatible graph analysis on an edge CSV.")
    ap.add_argument("edge_csv"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target")
    ap.add_argument("--require-networkx", action="store_true"); ap.add_argument("--output")
    args = ap.parse_args()
    result = analyse(Path(args.edge_csv), args.source_col, args.target_col, args.require_networkx)
    if args.output: Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
