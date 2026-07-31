#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['review_id','time_utc','subject','source','headline','date','theme','severity','credibility','locator','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'review_id':str(uuid.uuid4()),'time_utc':now(),'subject':a.subject,'source':a.source,'headline':a.headline,'date':a.date,'theme':a.theme,'severity':a.severity,'credibility':a.credibility,'locator':a.locator,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record media and news review findings with source, theme, severity, and credibility.')
    ap.add_argument('review'); ap.add_argument('--subject',required=True); ap.add_argument('--source',default=''); ap.add_argument('--headline',default=''); ap.add_argument('--date',default=''); ap.add_argument('--theme',default=''); ap.add_argument('--severity',default='low'); ap.add_argument('--credibility',default='unknown'); ap.add_argument('--locator',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.review)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
