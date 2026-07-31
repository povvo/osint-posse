#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['filing_id','time_utc','portal','entity','filing_name','filing_date','period','material_points','locator','review_status','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'filing_id':str(uuid.uuid4()),'time_utc':now(),'portal':a.portal,'entity':a.entity,'filing_name':a.filing_name,'filing_date':a.filing_date,'period':a.period,'material_points':a.material_points,'locator':a.locator,'review_status':a.review_status,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Track filings, accounts, officer records, and material disclosures from filing portals.')
    ap.add_argument('tracker'); ap.add_argument('--portal',required=True); ap.add_argument('--entity',required=True); ap.add_argument('--filing-name',required=True); ap.add_argument('--filing-date',default=''); ap.add_argument('--period',default=''); ap.add_argument('--material-points',default=''); ap.add_argument('--locator',default=''); ap.add_argument('--review-status',default='pending'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.tracker)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
