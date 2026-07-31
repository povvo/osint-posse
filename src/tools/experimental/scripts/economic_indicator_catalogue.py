#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from pathlib import Path

FIELDS=['indicator_id','database','indicator','geography','periodicity','unit','locator','definition','notes']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path,args):
    rows=read(path); row={'indicator_id':str(uuid.uuid4()),'database':args.database,'indicator':args.indicator,'geography':args.geography,'periodicity':args.periodicity,'unit':args.unit,'locator':args.locator,'definition':args.definition,'notes':args.notes}
    rows.append(row); save(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Catalogue economic indicator datasets and definitions.')
    p.add_argument('catalogue'); p.add_argument('--database'); p.add_argument('--indicator'); p.add_argument('--geography', default=''); p.add_argument('--periodicity', default=''); p.add_argument('--unit', default=''); p.add_argument('--locator', default=''); p.add_argument('--definition', default=''); p.add_argument('--notes', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.catalogue)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    if not a.database or not a.indicator: p.error('--database and --indicator are required unless --list is used')
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
