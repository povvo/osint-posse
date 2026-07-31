#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, itertools, json
from pathlib import Path


def read_dimensions(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def build(rows, output: Path):
    dims={}
    for r in rows:
        dims.setdefault(r.get('dimension',''),[]).append(r.get('option',''))
    dims={k:[v for v in vals if v] for k,vals in dims.items() if k}
    fields=list(dims)
    combos=[dict(zip(fields, vals)) for vals in itertools.product(*(dims[f] for f in fields))] if fields else []
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields+['plausibility','notes'], extrasaction='ignore'); w.writeheader()
        for c in combos: c.update({'plausibility':'unrated','notes':''}); w.writerow(c)
    return {'output':str(output),'dimensions':len(fields),'combinations':len(combos)}

def init(path: Path):
    fields=['dimension','option','definition']
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows([{'dimension':'actor','option':'A','definition':''},{'dimension':'mechanism','option':'B','definition':''}])
    return {'created':str(path),'fields':fields}

def main():
    p=argparse.ArgumentParser(description='Create morphological-analysis option matrices and scenario combinations.')
    p.add_argument('--init'); p.add_argument('--dimensions'); p.add_argument('--output', default='morphological_matrix.csv')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)), indent=2)); return 0
    if not a.dimensions: p.error('use --init or --dimensions')
    print(json.dumps(build(read_dimensions(Path(a.dimensions)), Path(a.output)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
