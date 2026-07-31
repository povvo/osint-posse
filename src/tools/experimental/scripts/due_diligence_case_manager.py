#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['case_id','time_utc','subject','case_type','risk_rating','status','owner','verification_summary','open_items','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'case_id':str(uuid.uuid4()),'time_utc':now(),'subject':a.subject,'case_type':a.case_type,'risk_rating':a.risk_rating,'status':a.status,'owner':a.owner,'verification_summary':a.verification_summary,'open_items':a.open_items,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Track due-diligence cases, risk ratings, owners, and open verification items.')
    ap.add_argument('cases'); ap.add_argument('--subject',required=True); ap.add_argument('--case-type',default='KYB'); ap.add_argument('--risk-rating',default='unrated'); ap.add_argument('--status',default='open'); ap.add_argument('--owner',default=''); ap.add_argument('--verification-summary',default=''); ap.add_argument('--open-items',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.cases)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
