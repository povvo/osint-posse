#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['request_id','time_utc','exchange','case_id','request_type','address_or_tx','sent_date','response_date','status','evidence_ref','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'request_id':str(uuid.uuid4()),'time_utc':now(),'exchange':a.exchange,'case_id':a.case_id,'request_type':a.request_type,'address_or_tx':a.address_or_tx,'sent_date':a.sent_date,'response_date':a.response_date,'status':a.status,'evidence_ref':a.evidence_ref,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Track exchange records requests, responses, and attributed evidence references.')
    ap.add_argument('tracker'); ap.add_argument('--exchange',required=True); ap.add_argument('--case-id',default=''); ap.add_argument('--request-type',default='records'); ap.add_argument('--address-or-tx',default=''); ap.add_argument('--sent-date',default=''); ap.add_argument('--response-date',default=''); ap.add_argument('--status',default='open'); ap.add_argument('--evidence-ref',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.tracker)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
