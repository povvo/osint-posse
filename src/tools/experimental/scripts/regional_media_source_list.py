#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from pathlib import Path

FIELDS=['source_id','region','language','source_name','url_or_locator','source_type','reliability_note','access_note','topic_tags']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path, args):
    rows=read(path); row={'source_id':str(uuid.uuid4()),'region':args.region,'language':args.language,'source_name':args.source_name,'url_or_locator':args.locator,'source_type':args.source_type,'reliability_note':args.reliability_note,'access_note':args.access_note,'topic_tags':';'.join(args.tag or [])}
    rows.append(row); save(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Maintain a regional media and local source list.')
    p.add_argument('list_csv'); p.add_argument('--region'); p.add_argument('--language', default=''); p.add_argument('--source-name'); p.add_argument('--locator', default=''); p.add_argument('--source-type', default='media'); p.add_argument('--reliability-note', default=''); p.add_argument('--access-note', default=''); p.add_argument('--tag', action='append'); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.list_csv)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    if not a.region or not a.source_name: p.error('--region and --source-name are required unless --list is used')
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
