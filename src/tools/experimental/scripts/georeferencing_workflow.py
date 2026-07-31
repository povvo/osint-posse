#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path

FIELDS=['point_id','source_x','source_y','target_lat','target_lon','residual','control_note']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def init(path: Path):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
    return {'created':str(path),'fields':FIELDS}

def audit(path: Path, threshold: float):
    rows=read(path); findings=[]
    for i,r in enumerate(rows,1):
        try:
            residual=float(r.get('residual',0) or 0)
            lat=float(r.get('target_lat',0) or 0); lon=float(r.get('target_lon',0) or 0)
            if residual>threshold: findings.append({'row':i,'issue':'high residual','residual':residual})
            if not (-90<=lat<=90 and -180<=lon<=180): findings.append({'row':i,'issue':'coordinate out of range'})
        except ValueError: findings.append({'row':i,'issue':'invalid numeric value'})
    return {'rows':len(rows),'findings':findings,'ok':not findings}

def main():
    p=argparse.ArgumentParser(description='Create or audit a georeferencing control-point workflow table.')
    p.add_argument('--init'); p.add_argument('--audit'); p.add_argument('--threshold', type=float, default=10.0)
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)), indent=2)); return 0
    if not a.audit: p.error('use --init or --audit')
    print(json.dumps(audit(Path(a.audit), a.threshold), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
