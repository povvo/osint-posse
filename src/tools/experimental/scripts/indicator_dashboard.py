#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, statistics
from collections import defaultdict
from pathlib import Path


def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def dashboard(input_csv: Path, indicator_col: str, value_col: str, output: Path):
    rows=read(input_csv); groups=defaultdict(list)
    for r in rows:
        try: groups[r.get(indicator_col,'unknown')].append(float(r.get(value_col,0) or 0))
        except ValueError: pass
    result={'indicator_count':len(groups),'indicators':[]}
    for k,vals in sorted(groups.items()):
        result['indicators'].append({'indicator':k,'count':len(vals),'min':min(vals),'max':max(vals),'mean':statistics.mean(vals)})
    output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    return {'output':str(output), 'indicator_count':len(groups)}

def main():
    p=argparse.ArgumentParser(description='Build a JSON dashboard summary for indicator values.')
    p.add_argument('input_csv'); p.add_argument('--indicator-col', default='indicator'); p.add_argument('--value-col', default='value'); p.add_argument('--output', default='indicator_dashboard.json')
    a=p.parse_args(); print(json.dumps(dashboard(Path(a.input_csv), a.indicator_col, a.value_col, Path(a.output)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
