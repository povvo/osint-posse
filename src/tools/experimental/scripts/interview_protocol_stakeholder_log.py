#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['entry_id','time_utc','stakeholder','role','question_set','contact_status','meeting_date','summary','follow_up','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'entry_id':str(uuid.uuid4()),'time_utc':now(),'stakeholder':a.stakeholder,'role':a.role,'question_set':a.question_set,'contact_status':a.contact_status,'meeting_date':a.meeting_date,'summary':a.summary,'follow_up':a.follow_up,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Track stakeholder interview protocol status and follow-up.')
    ap.add_argument('log'); ap.add_argument('--stakeholder'); ap.add_argument('--role',default=''); ap.add_argument('--question-set',default=''); ap.add_argument('--contact-status',default='planned'); ap.add_argument('--meeting-date',default=''); ap.add_argument('--summary',default=''); ap.add_argument('--follow-up',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    if not a.stakeholder: ap.error('--stakeholder is required unless --list is used')
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
