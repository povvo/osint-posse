#!/usr/bin/env python3
"""Community detection script.

Runs standard-library connected-component detection and optional NetworkX greedy
modularity communities when NetworkX is available.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict, deque
from pathlib import Path


def read_edges(path: Path, source_col: str, target_col: str) -> list[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [(r[source_col], r[target_col]) for r in csv.DictReader(handle) if r.get(source_col) and r.get(target_col)]


def fallback(edges: list[tuple[str, str]]) -> list[list[str]]:
    adj: dict[str, set[str]] = defaultdict(set)
    for a, b in edges: adj[a].add(b); adj[b].add(a)
    seen, communities = set(), []
    for node in sorted(adj):
        if node in seen: continue
        queue, group = deque([node]), []
        seen.add(node)
        while queue:
            cur = queue.popleft(); group.append(cur)
            for nxt in adj[cur]:
                if nxt not in seen: seen.add(nxt); queue.append(nxt)
        communities.append(sorted(group))
    return communities


def detect(edges: list[tuple[str, str]]) -> dict:
    try:
        import networkx as nx  # type: ignore
        graph = nx.Graph(); graph.add_edges_from(edges)
        groups = [sorted(c) for c in nx.community.greedy_modularity_communities(graph)]
        engine = "networkx_greedy_modularity"
    except Exception:
        groups = fallback(edges); engine = "connected_components"
    return {"engine": engine, "community_count": len(groups), "communities": [{"id": i + 1, "size": len(g), "nodes": g} for i, g in enumerate(groups)]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect communities in an edge CSV.")
    ap.add_argument("edge_csv"); ap.add_argument("--source-col", default="source"); ap.add_argument("--target-col", default="target"); ap.add_argument("--output", default="communities.json")
    args = ap.parse_args()
    result = detect(read_edges(Path(args.edge_csv), args.source_col, args.target_col))
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "community_count": result["community_count"], "engine": result["engine"]}, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
