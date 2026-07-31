#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['review_id','time_utc','place','imagery_source','capture_date','locator','terrain_note','structure_note','confidence','reviewer','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'review_id':str(uuid.uuid4()),'time_utc':now(),'place':a.place,'imagery_source':a.imagery_source,'capture_date':a.capture_date,'locator':a.locator,'terrain_note':a.terrain_note,'structure_note':a.structure_note,'confidence':a.confidence,'reviewer':a.reviewer,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record place imagery review observations and confidence notes.')
    ap.add_argument('log'); ap.add_argument('--place',required=True); ap.add_argument('--imagery-source',default=''); ap.add_argument('--capture-date',default=''); ap.add_argument('--locator',default=''); ap.add_argument('--terrain-note',default=''); ap.add_argument('--structure-note',default=''); ap.add_argument('--confidence',default='low'); ap.add_argument('--reviewer',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
