#!/usr/bin/env python3
"""NetworkX / Python notebooks.

Creates a reproducible Python notebook-style Markdown scaffold and companion script
for graph metrics, charts, and review notes.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def create(edge_csv: str, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    md = output_dir / "networkx_analysis_notebook.md"
    py = output_dir / "networkx_analysis.py"
    md.write_text(f"""# NetworkX Analysis Notebook

Input edge CSV: `{edge_csv}`

## Setup

```python
import csv
from pathlib import Path
edge_csv = Path({edge_csv!r})
```

## Questions

- Which nodes are central?
- Which components are isolated?
- Which edges require source review?

## Findings

-
""", encoding="utf-8")
    py.write_text("""from pathlib import Path
import csv, json
edge_csv = Path(%r)
with edge_csv.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
print(json.dumps({'rows': len(rows), 'fields': list(rows[0]) if rows else []}, indent=2))
""" % edge_csv, encoding="utf-8")
    return {"markdown": str(md), "script": str(py)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a NetworkX/Python notebook scaffold.")
    ap.add_argument("edge_csv"); ap.add_argument("--output-dir", default="networkx_notebook")
    args = ap.parse_args()
    print(json.dumps(create(args.edge_csv, Path(args.output_dir)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
