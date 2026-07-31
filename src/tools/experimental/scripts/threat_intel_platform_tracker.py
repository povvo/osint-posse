#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['object_id','time_utc','platform','object_type','value','relationship','report','campaign','confidence','source_ref','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'object_id':str(uuid.uuid4()),'time_utc':now(),'platform':a.platform,'object_type':a.object_type,'value':a.value,'relationship':a.relationship,'report':a.report,'campaign':a.campaign,'confidence':a.confidence,'source_ref':a.source_ref,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Track threat intelligence objects, sightings, reports, campaigns, and relationships.')
    ap.add_argument('tracker'); ap.add_argument('--platform',default=''); ap.add_argument('--object-type',required=True); ap.add_argument('--value',required=True); ap.add_argument('--relationship',default=''); ap.add_argument('--report',default=''); ap.add_argument('--campaign',default=''); ap.add_argument('--confidence',default='low'); ap.add_argument('--source-ref',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.tracker)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
