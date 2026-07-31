#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS=['map_id','map_title','image_file','control_points_file','target_crs','georef_file','residual_mean','review_status','notes']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path,args):
    rows=read(path); row={field:getattr(args, field) for field in ['map_id','map_title','image_file','control_points_file','target_crs','georef_file','residual_mean','review_status','notes']}
    rows.append(row); save(path, rows); return row

def audit(path, max_residual):
    findings=[]; rows=read(path)
    for i,r in enumerate(rows,1):
        try:
            if float(r.get('residual_mean') or 0)>max_residual: findings.append({'row':i,'issue':'mean residual above threshold'})
        except ValueError: findings.append({'row':i,'issue':'invalid residual_mean'})
        for field in ['image_file','control_points_file','georef_file']:
            if r.get(field) and not Path(r[field]).exists(): findings.append({'row':i,'issue':f'{field} not found'})
    return {'rows':len(rows),'findings':findings,'ok':not findings}

def main():
    p=argparse.ArgumentParser(description='Track historical map georeferencing work and residual review.')
    sub=p.add_subparsers(dest='cmd', required=True)
    a=sub.add_parser('add'); a.add_argument('log')
    for f in FIELDS: a.add_argument('--'+f.replace('_','-'), default='')
    au=sub.add_parser('audit'); au.add_argument('log'); au.add_argument('--max-residual', type=float, default=10)
    l=sub.add_parser('list'); l.add_argument('log')
    args=p.parse_args()
    if args.cmd=='add': print(json.dumps(add(Path(args.log), args), indent=2)); return 0
    if args.cmd=='audit': print(json.dumps(audit(Path(args.log), args.max_residual), indent=2)); return 0
    print(json.dumps(read(Path(args.log)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
