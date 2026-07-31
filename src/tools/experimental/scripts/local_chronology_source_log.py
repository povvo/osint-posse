#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['event_id','time_utc','date','place','event','source_ref','confidence','uncertainty','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'event_id':str(uuid.uuid4()),'time_utc':now(),'date':a.date,'place':a.place,'event':a.event,'source_ref':a.source_ref,'confidence':a.confidence,'uncertainty':a.uncertainty,'notes':a.notes}; rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Maintain a local chronology with source references and uncertainty notes.')
    ap.add_argument('log'); ap.add_argument('--date',required=True); ap.add_argument('--place',default=''); ap.add_argument('--event',required=True); ap.add_argument('--source-ref',default=''); ap.add_argument('--confidence',default='low'); ap.add_argument('--uncertainty',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
