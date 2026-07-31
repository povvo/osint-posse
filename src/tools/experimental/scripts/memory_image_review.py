#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['review_id','time_utc','image_file','profile','process_note','network_note','module_note','finding','reviewer','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'review_id':str(uuid.uuid4()),'time_utc':now(),'image_file':a.image_file,'profile':a.profile,'process_note':a.process_note,'network_note':a.network_note,'module_note':a.module_note,'finding':a.finding,'reviewer':a.reviewer,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record memory image review notes for processes, network data, modules, and findings.')
    ap.add_argument('log'); ap.add_argument('--image-file',required=True); ap.add_argument('--profile',default=''); ap.add_argument('--process-note',default=''); ap.add_argument('--network-note',default=''); ap.add_argument('--module-note',default=''); ap.add_argument('--finding',default=''); ap.add_argument('--reviewer',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
