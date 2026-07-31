#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path


def create(input_csv: str, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    py=output_dir/'analysis_notebook.py'; md=output_dir/'analysis_notebook.md'
    py.write_text("""from pathlib import Path
import csv, json, statistics
csv_path = Path(%r)
with csv_path.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
print(json.dumps({'rows': len(rows), 'fields': list(rows[0]) if rows else []}, indent=2))
""" % input_csv, encoding='utf-8')
    md.write_text(f"# Statistical Analysis Notebook\n\nInput: `{input_csv}`\n\n## Questions\n\n- What distributions matter?\n- Which fields need cleaning?\n- Which assumptions affect interpretation?\n", encoding='utf-8')
    return {'script':str(py),'markdown':str(md)}

def main():
    p=argparse.ArgumentParser(description='Create an R/Stata/Python-style statistical notebook scaffold.')
    p.add_argument('input_csv'); p.add_argument('--output-dir', default='statistical_notebook')
    a=p.parse_args(); print(json.dumps(create(a.input_csv, Path(a.output_dir)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
