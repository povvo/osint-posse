#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['record_id','time_utc','title','record_class','owner','locator','retention_rule','access_rule','status','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'record_id':str(uuid.uuid4()),'time_utc':now(),'title':a.title,'record_class':a.record_class,'owner':a.owner,'locator':a.locator,'retention_rule':a.retention_rule,'access_rule':a.access_rule,'status':a.status,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Maintain an electronic document and records index.')
    ap.add_argument('index'); ap.add_argument('--title'); ap.add_argument('--record-class',default='general'); ap.add_argument('--owner',default=''); ap.add_argument('--locator',default=''); ap.add_argument('--retention-rule',default=''); ap.add_argument('--access-rule',default='standard'); ap.add_argument('--status',default='active'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.index)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    if not a.title: ap.error('--title required unless --list is used')
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
