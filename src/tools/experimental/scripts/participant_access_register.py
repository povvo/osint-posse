#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['entry_id','time_utc','person_ref','project','permission_scope','access_rule','review_date','status','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'entry_id':str(uuid.uuid4()),'time_utc':now(),'person_ref':a.person_ref,'project':a.project,'permission_scope':a.permission_scope,'access_rule':a.access_rule,'review_date':a.review_date,'status':a.status,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Maintain a participant permission and access register.')
    ap.add_argument('register'); ap.add_argument('--person-ref'); ap.add_argument('--project',default=''); ap.add_argument('--permission-scope',default=''); ap.add_argument('--access-rule',default='restricted'); ap.add_argument('--review-date',default=''); ap.add_argument('--status',default='active'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.register)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    if not a.person_ref: ap.error('--person-ref is required unless --list is used')
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
