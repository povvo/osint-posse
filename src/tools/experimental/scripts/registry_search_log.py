#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['id','time_utc','registry','record_type','subject','query','result','locator','basis_note','next_step']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'id':str(uuid.uuid4()),'time_utc':now(),'registry':a.registry,'record_type':a.record_type,'subject':a.subject,'query':a.query,'result':a.result,'locator':a.locator,'basis_note':a.basis_note,'next_step':a.next_step}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record registry search actions and results.')
    ap.add_argument('log'); ap.add_argument('--registry'); ap.add_argument('--record-type',default=''); ap.add_argument('--subject',default=''); ap.add_argument('--query'); ap.add_argument('--result',default=''); ap.add_argument('--locator',default=''); ap.add_argument('--basis-note',default=''); ap.add_argument('--next-step',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    if not a.registry or not a.query: ap.error('--registry and --query are required unless --list is used')
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
