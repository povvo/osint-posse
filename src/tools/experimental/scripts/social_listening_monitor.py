#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['monitor_id','time_utc','source','query','theme','volume','sentiment','alert_level','sample_locator','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'monitor_id':str(uuid.uuid4()),'time_utc':now(),'source':a.source,'query':a.query,'theme':a.theme,'volume':a.volume,'sentiment':a.sentiment,'alert_level':a.alert_level,'sample_locator':a.sample_locator,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record public-content monitoring observations, themes, volume, and alert levels.')
    ap.add_argument('log'); ap.add_argument('--source',required=True); ap.add_argument('--query',required=True); ap.add_argument('--theme',default=''); ap.add_argument('--volume',default=''); ap.add_argument('--sentiment',default='unknown'); ap.add_argument('--alert-level',default='normal'); ap.add_argument('--sample-locator',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
