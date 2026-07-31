#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read_table(path: Path) -> list[dict]:
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def write_table(path: Path, data: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)


def export(edge_csv: Path, output_dir: Path, source_col: str, target_col: str) -> dict:
    edges = [row for row in read_table(edge_csv) if row.get(source_col) and row.get(target_col)]
    nodes: dict[str, dict] = {}
    for row in edges:
        nodes.setdefault(row[source_col], {'id': row[source_col], 'label': row[source_col]})
        nodes.setdefault(row[target_col], {'id': row[target_col], 'label': row[target_col]})
    node_rows = sorted(nodes.values(), key=lambda item: item['id'])
    output_dir.mkdir(parents=True, exist_ok=True)
    node_path, edge_path = output_dir / 'nodes.csv', output_dir / 'edges.csv'
    write_table(node_path, node_rows, ['id', 'label'])
    write_table(edge_path, edges, [source_col, target_col])
    return {'node_csv': str(node_path), 'edge_csv': str(edge_path), 'node_count': len(node_rows), 'edge_count': len(edges)}


def main() -> int:
    parser = argparse.ArgumentParser(description='Create node and edge CSV files for visual graph review.')
    parser.add_argument('edge_csv')
    parser.add_argument('--output-dir', default='visual_graph_export')
    parser.add_argument('--source-col', default='source')
    parser.add_argument('--target-col', default='target')
    args = parser.parse_args()
    print(json.dumps(export(Path(args.edge_csv), Path(args.output_dir), args.source_col, args.target_col), indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
