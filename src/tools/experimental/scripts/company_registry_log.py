#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['record_id','time_utc','registry','company_name','company_number','jurisdiction','filing_type','filing_date','director_or_owner','locator','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'record_id':str(uuid.uuid4()),'time_utc':now(),'registry':a.registry,'company_name':a.company_name,'company_number':a.company_number,'jurisdiction':a.jurisdiction,'filing_type':a.filing_type,'filing_date':a.filing_date,'director_or_owner':a.director_or_owner,'locator':a.locator,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record company registry lookups, filings, directors, owners, and locators.')
    ap.add_argument('log'); ap.add_argument('--registry',required=True); ap.add_argument('--company-name',required=True); ap.add_argument('--company-number',default=''); ap.add_argument('--jurisdiction',default=''); ap.add_argument('--filing-type',default=''); ap.add_argument('--filing-date',default=''); ap.add_argument('--director-or-owner',default=''); ap.add_argument('--locator',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
