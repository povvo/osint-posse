#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['entry_id','time_utc','case_id','decision','risk','reason','rejected_option','mitigation','owner','review_date','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'entry_id':str(uuid.uuid4()),'time_utc':now(),'case_id':a.case_id,'decision':a.decision,'risk':a.risk,'reason':a.reason,'rejected_option':a.rejected_option,'mitigation':a.mitigation,'owner':a.owner,'review_date':a.review_date,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record risk decisions, rejected options, mitigations, and review dates.')
    ap.add_argument('log'); ap.add_argument('--case-id',default=''); ap.add_argument('--decision',required=True); ap.add_argument('--risk',default=''); ap.add_argument('--reason',default=''); ap.add_argument('--rejected-option',default=''); ap.add_argument('--mitigation',default=''); ap.add_argument('--owner',default=''); ap.add_argument('--review-date',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
