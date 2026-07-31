#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from pathlib import Path
FIELDS=['asset_id','name','owner','record_class','location','format','sensitivity','retention','risk','notes']
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'asset_id':str(uuid.uuid4()),'name':a.name,'owner':a.owner,'record_class':a.record_class,'location':a.location,'format':a.format,'sensitivity':a.sensitivity,'retention':a.retention,'risk':a.risk,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def summary(p):
    rows=read(p)
    return {'assets':len(rows),'high_risk':sum(1 for r in rows if str(r.get('risk','')).lower()=='high'),'sensitive':sum(1 for r in rows if str(r.get('sensitivity','')).lower() in {'restricted','sensitive','high'})}
def main():
    ap=argparse.ArgumentParser(description='Maintain an information asset register.')
    sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('add'); a.add_argument('register'); a.add_argument('--name',required=True); a.add_argument('--owner',default=''); a.add_argument('--record-class',default=''); a.add_argument('--location',default=''); a.add_argument('--format',default=''); a.add_argument('--sensitivity',default='internal'); a.add_argument('--retention',default=''); a.add_argument('--risk',default=''); a.add_argument('--notes',default='')
    s=sub.add_parser('summary'); s.add_argument('register')
    l=sub.add_parser('list'); l.add_argument('register')
    args=ap.parse_args()
    if args.cmd=='add': print(json.dumps(add(Path(args.register),args),indent=2)); return 0
    if args.cmd=='summary': print(json.dumps(summary(Path(args.register)),indent=2)); return 0
    print(json.dumps(read(Path(args.register)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
