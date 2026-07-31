#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['note_id','time_utc','case_id','typology','indicator','narrative','supporting_ref','escalation','reviewer','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'note_id':str(uuid.uuid4()),'time_utc':now(),'case_id':a.case_id,'typology':a.typology,'indicator':a.indicator,'narrative':a.narrative,'supporting_ref':a.supporting_ref,'escalation':a.escalation,'reviewer':a.reviewer,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record financial-crime case notes, indicators, narrative, evidence, and escalation status.')
    ap.add_argument('notes_file'); ap.add_argument('--case-id',default=''); ap.add_argument('--typology',default=''); ap.add_argument('--indicator',default=''); ap.add_argument('--narrative',required=True); ap.add_argument('--supporting-ref',default=''); ap.add_argument('--escalation',default='review'); ap.add_argument('--reviewer',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.notes_file)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
