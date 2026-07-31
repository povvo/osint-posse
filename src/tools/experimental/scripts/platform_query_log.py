#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['query_id','time_utc','platform','query','scope','parameters','result_count','capture_ref','permission_note','next_action']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'query_id':str(uuid.uuid4()),'time_utc':now(),'platform':a.platform,'query':a.query,'scope':a.scope,'parameters':a.parameters,'result_count':a.result_count,'capture_ref':a.capture_ref,'permission_note':a.permission_note,'next_action':a.next_action}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record public platform query parameters and result notes.')
    ap.add_argument('log'); ap.add_argument('--platform',required=True); ap.add_argument('--query',required=True); ap.add_argument('--scope',default='public'); ap.add_argument('--parameters',default=''); ap.add_argument('--result-count',default=''); ap.add_argument('--capture-ref',default=''); ap.add_argument('--permission-note',default=''); ap.add_argument('--next-action',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
