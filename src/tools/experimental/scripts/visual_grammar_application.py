#!/usr/bin/env python3
"""Visual Grammar Application.

Applies consistent visual rules to node and edge CSVs by assigning shapes,
colours as text labels, line styles, and legend entries for review tools.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

NODE_RULES = {"person": ("circle", "blue"), "organisation": ("square", "green"), "place": ("triangle", "orange"), "event": ("diamond", "purple"), "asset": ("hexagon", "grey")}
EDGE_RULES = {"owns": "solid", "controls": "bold", "associated_with": "dashed", "located_at": "dotted"}


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    fields = sorted({k for r in rows for k in r}) if rows else ["id"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def apply(nodes_csv: Path, edges_csv: Path, output_dir: Path) -> dict:
    nodes = read(nodes_csv); edges = read(edges_csv)
    for node in nodes:
        shape, colour = NODE_RULES.get(str(node.get("type", "")).lower(), ("circle", "black"))
        node["viz_shape"] = shape; node["viz_colour_label"] = colour
    for edge in edges:
        edge["viz_line_style"] = EDGE_RULES.get(str(edge.get("relationship", "")).lower(), "solid")
    output_dir.mkdir(parents=True, exist_ok=True)
    write(output_dir / "visual_nodes.csv", nodes); write(output_dir / "visual_edges.csv", edges)
    legend = {"node_rules": NODE_RULES, "edge_rules": EDGE_RULES}
    (output_dir / "visual_legend.json").write_text(json.dumps(legend, indent=2), encoding="utf-8")
    return {"nodes": len(nodes), "edges": len(edges), "output_dir": str(output_dir)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply visual grammar fields to graph CSVs.")
    ap.add_argument("--nodes", required=True); ap.add_argument("--edges", required=True); ap.add_argument("--output-dir", default="visual_grammar")
    args = ap.parse_args()
    print(json.dumps(apply(Path(args.nodes), Path(args.edges), Path(args.output_dir)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
