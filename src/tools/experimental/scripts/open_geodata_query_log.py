#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['query_id','time_utc','dataset','area','feature_type','query_text','result_file','licence','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'query_id':str(uuid.uuid4()),'time_utc':now(),'dataset':a.dataset,'area':a.area,'feature_type':a.feature_type,'query_text':a.query_text,'result_file':a.result_file,'licence':a.licence,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record open geodata query text, areas, feature types, and result files.')
    ap.add_argument('log'); ap.add_argument('--dataset',default='OSM'); ap.add_argument('--area',required=True); ap.add_argument('--feature-type',default=''); ap.add_argument('--query-text',default=''); ap.add_argument('--result-file',default=''); ap.add_argument('--licence',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
