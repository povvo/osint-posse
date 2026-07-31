#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['observation_id','time_utc','sample','environment','action','file_note','network_note','process_note','persistence_note','review_status','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'observation_id':str(uuid.uuid4()),'time_utc':now(),'sample':a.sample,'environment':a.environment,'action':a.action,'file_note':a.file_note,'network_note':a.network_note,'process_note':a.process_note,'persistence_note':a.persistence_note,'review_status':a.review_status,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record isolated sample behaviour observations and review notes.')
    ap.add_argument('log'); ap.add_argument('--sample',required=True); ap.add_argument('--environment',default='isolated'); ap.add_argument('--action',default='observed'); ap.add_argument('--file-note',default=''); ap.add_argument('--network-note',default=''); ap.add_argument('--process-note',default=''); ap.add_argument('--persistence-note',default=''); ap.add_argument('--review-status',default='pending'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
