#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['request_id','time_utc','area_of_interest','date_range','sensor','cloud_limit','purpose','locator','status','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'request_id':str(uuid.uuid4()),'time_utc':now(),'area_of_interest':a.area_of_interest,'date_range':a.date_range,'sensor':a.sensor,'cloud_limit':a.cloud_limit,'purpose':a.purpose,'locator':a.locator,'status':a.status,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record satellite imagery search requests and source locators.')
    ap.add_argument('log'); ap.add_argument('--area-of-interest',required=True); ap.add_argument('--date-range',default=''); ap.add_argument('--sensor',default=''); ap.add_argument('--cloud-limit',default=''); ap.add_argument('--purpose',default=''); ap.add_argument('--locator',default=''); ap.add_argument('--status',default='requested'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
