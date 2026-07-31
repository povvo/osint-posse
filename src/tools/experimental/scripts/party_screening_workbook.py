#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['screen_id','time_utc','party','party_type','source_list','match_name','match_status','score','review_decision','source_ref','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'screen_id':str(uuid.uuid4()),'time_utc':now(),'party':a.party,'party_type':a.party_type,'source_list':a.source_list,'match_name':a.match_name,'match_status':a.match_status,'score':a.score,'review_decision':a.review_decision,'source_ref':a.source_ref,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record party, owner, vessel, address, and counterparty screening decisions.')
    ap.add_argument('workbook'); ap.add_argument('--party',required=True); ap.add_argument('--party-type',default='entity'); ap.add_argument('--source-list',default=''); ap.add_argument('--match-name',default=''); ap.add_argument('--match-status',default='pending'); ap.add_argument('--score',default=''); ap.add_argument('--review-decision',default='review'); ap.add_argument('--source-ref',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.workbook)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
