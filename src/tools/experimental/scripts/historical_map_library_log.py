#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from pathlib import Path

FIELDS=['map_id','library','title','date','scale','coverage','locator','rights','georef_status','notes']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path, args):
    rows=read(path); row={'map_id':str(uuid.uuid4()),'library':args.library,'title':args.title,'date':args.date,'scale':args.scale,'coverage':args.coverage,'locator':args.locator,'rights':args.rights,'georef_status':args.georef_status,'notes':args.notes}
    rows.append(row); save(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Record historical map library searches and georeferencing status.')
    p.add_argument('log'); p.add_argument('--library'); p.add_argument('--title'); p.add_argument('--date', default=''); p.add_argument('--scale', default=''); p.add_argument('--coverage', default=''); p.add_argument('--locator', default=''); p.add_argument('--rights', default=''); p.add_argument('--georef-status', default='not_started'); p.add_argument('--notes', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.log)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    if not a.library or not a.title: p.error('--library and --title are required unless --list is used')
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
