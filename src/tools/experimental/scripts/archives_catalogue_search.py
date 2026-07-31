#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, re, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS=['search_id','time_utc','catalogue','collection','reference','query','date_range','result_summary','access_note','next_action']

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path,args):
    rows=read(path); row={'search_id':str(uuid.uuid4()),'time_utc':now(),'catalogue':args.catalogue,'collection':args.collection,'reference':args.reference,'query':args.query,'date_range':args.date_range,'result_summary':args.result_summary,'access_note':args.access_note,'next_action':args.next_action}
    rows.append(row); save(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Record archive and catalogue searches with references and next actions.')
    p.add_argument('log'); p.add_argument('--catalogue'); p.add_argument('--collection', default=''); p.add_argument('--reference', default=''); p.add_argument('--query'); p.add_argument('--date-range', default=''); p.add_argument('--result-summary', default=''); p.add_argument('--access-note', default=''); p.add_argument('--next-action', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.log)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    if not a.catalogue or not a.query: p.error('--catalogue and --query required unless --list is used')
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
