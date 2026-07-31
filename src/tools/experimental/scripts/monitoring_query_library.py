#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from pathlib import Path
FIELDS=['query_id','name','query','trigger','severity','owner','enabled','review_cycle','notes']
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'query_id':str(uuid.uuid4()),'name':a.name,'query':a.query,'trigger':a.trigger,'severity':a.severity,'owner':a.owner,'enabled':a.enabled,'review_cycle':a.review_cycle,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Maintain query, trigger, and escalation records for public monitoring.')
    ap.add_argument('library'); ap.add_argument('--name',required=True); ap.add_argument('--query',required=True); ap.add_argument('--trigger',default='new item'); ap.add_argument('--severity',default='normal'); ap.add_argument('--owner',default=''); ap.add_argument('--enabled',default='yes'); ap.add_argument('--review-cycle',default='weekly'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.library)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
