#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from pathlib import Path

FIELDS=['record_id','portal','parcel_or_address','record_type','reference','date','party','summary','locator','follow_up']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path,args):
    rows=read(path); row={'record_id':str(uuid.uuid4()),'portal':args.portal,'parcel_or_address':args.parcel_or_address,'record_type':args.record_type,'reference':args.reference,'date':args.date,'party':args.party,'summary':args.summary,'locator':args.locator,'follow_up':args.follow_up}
    rows.append(row); save(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Track land, property, and planning record searches.')
    p.add_argument('log'); p.add_argument('--portal'); p.add_argument('--parcel-or-address'); p.add_argument('--record-type', default='planning'); p.add_argument('--reference', default=''); p.add_argument('--date', default=''); p.add_argument('--party', default=''); p.add_argument('--summary', default=''); p.add_argument('--locator', default=''); p.add_argument('--follow-up', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.log)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    if not a.portal or not a.parcel_or_address: p.error('--portal and --parcel-or-address are required unless --list is used')
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
