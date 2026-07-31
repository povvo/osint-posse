#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['enrich_id','time_utc','indicator_type','value','hash_sha256','portal','detection_summary','relationship_note','confidence','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def digest(v): return hashlib.sha256(v.encode('utf-8')).hexdigest()
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'enrich_id':str(uuid.uuid4()),'time_utc':now(),'indicator_type':a.indicator_type,'value':a.value,'hash_sha256':digest(a.value),'portal':a.portal,'detection_summary':a.detection_summary,'relationship_note':a.relationship_note,'confidence':a.confidence,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record file, URL, domain, or IP enrichment results and relationship notes.')
    ap.add_argument('log'); ap.add_argument('--indicator-type',required=True); ap.add_argument('--value',required=True); ap.add_argument('--portal',default=''); ap.add_argument('--detection-summary',default=''); ap.add_argument('--relationship-note',default=''); ap.add_argument('--confidence',default='low'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
