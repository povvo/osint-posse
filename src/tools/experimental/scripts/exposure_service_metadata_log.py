#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['lookup_id','time_utc','asset','service','port','banner','location','provider','risk_note','source_ref','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'lookup_id':str(uuid.uuid4()),'time_utc':now(),'asset':a.asset,'service':a.service,'port':a.port,'banner':a.banner,'location':a.location,'provider':a.provider,'risk_note':a.risk_note,'source_ref':a.source_ref,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record lawful infrastructure exposure and service metadata observations.')
    ap.add_argument('log'); ap.add_argument('--asset',required=True); ap.add_argument('--service',default=''); ap.add_argument('--port',default=''); ap.add_argument('--banner',default=''); ap.add_argument('--location',default=''); ap.add_argument('--provider',default=''); ap.add_argument('--risk-note',default=''); ap.add_argument('--source-ref',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
