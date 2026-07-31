#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['search_id','time_utc','platform','query','account_or_topic','result_summary','capture_ref','status','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'search_id':str(uuid.uuid4()),'time_utc':now(),'platform':a.platform,'query':a.query,'account_or_topic':a.account_or_topic,'result_summary':a.result_summary,'capture_ref':a.capture_ref,'status':a.status,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record platform search actions, captures, and review notes.')
    ap.add_argument('log'); ap.add_argument('--platform'); ap.add_argument('--query'); ap.add_argument('--account-or-topic',default=''); ap.add_argument('--result-summary',default=''); ap.add_argument('--capture-ref',default=''); ap.add_argument('--status',default='pending'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    if not a.platform or not a.query: ap.error('--platform and --query are required unless --list is used')
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
