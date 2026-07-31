#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math, statistics
from pathlib import Path


def read(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def dist(a,b):
    return math.hypot(float(a.get('x',a.get('lon',0)))-float(b.get('x',b.get('lon',0))), float(a.get('y',a.get('lat',0)))-float(b.get('y',b.get('lat',0))))

def moran(rows, value_col: str, threshold: float):
    values=[float(r.get(value_col,0) or 0) for r in rows]
    mean=statistics.mean(values) if values else 0
    denom=sum((v-mean)**2 for v in values)
    weight_sum=0; num=0
    for i,a in enumerate(rows):
        for j,b in enumerate(rows):
            if i==j: continue
            w=1 if dist(a,b)<=threshold else 0
            weight_sum+=w; num+=w*(values[i]-mean)*(values[j]-mean)
    return (len(rows)/weight_sum)*(num/denom) if rows and weight_sum and denom else 0

def analyse(path: Path, value_col: str, threshold: float, output: Path):
    rows=read(path); result={'rows':len(rows),'value_col':value_col,'distance_threshold':threshold,'moran_i':round(moran(rows,value_col,threshold),6)}
    output.write_text(json.dumps(result, indent=2), encoding='utf-8'); return result

def main():
    p=argparse.ArgumentParser(description='Run a simple local spatial autocorrelation diagnostic on coordinate CSV rows.')
    p.add_argument('csv'); p.add_argument('--value-col', required=True); p.add_argument('--threshold', type=float, default=1.0); p.add_argument('--output', default='spatial_econometrics.json')
    a=p.parse_args(); print(json.dumps(analyse(Path(a.csv), a.value_col, a.threshold, Path(a.output)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
