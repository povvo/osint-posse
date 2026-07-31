#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['screen_id','time_utc','subject','screening_type','list_source','match_status','match_score','basis','reviewer','decision','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'screen_id':str(uuid.uuid4()),'time_utc':now(),'subject':a.subject,'screening_type':a.screening_type,'list_source':a.list_source,'match_status':a.match_status,'match_score':a.match_score,'basis':a.basis,'reviewer':a.reviewer,'decision':a.decision,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record compliance screening results, decisions, and review notes.')
    ap.add_argument('register'); ap.add_argument('--subject',required=True); ap.add_argument('--screening-type',default='party'); ap.add_argument('--list-source',default=''); ap.add_argument('--match-status',default='pending'); ap.add_argument('--match-score',default=''); ap.add_argument('--basis',default=''); ap.add_argument('--reviewer',default=''); ap.add_argument('--decision',default='review'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.register)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
