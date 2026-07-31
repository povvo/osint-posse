#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS=['dataset_id','time_utc','portal','dataset_name','indicator','geography','period','locator','licence','notes']

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def read(p: Path):
    if not p.exists(): return []
    with p.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def write(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(p: Path, a):
    rows=read(p); row={'dataset_id':str(uuid.uuid4()),'time_utc':now(),'portal':a.portal,'dataset_name':a.dataset_name,'indicator':a.indicator,'geography':a.geography,'period':a.period,'locator':a.locator,'licence':a.licence,'notes':a.notes}
    rows.append(row); write(p, rows); return row

def main():
    p=argparse.ArgumentParser(description='Catalogue national statistics and census datasets for later analysis.')
    p.add_argument('catalogue'); p.add_argument('--portal'); p.add_argument('--dataset-name'); p.add_argument('--indicator', default=''); p.add_argument('--geography', default=''); p.add_argument('--period', default=''); p.add_argument('--locator', default=''); p.add_argument('--licence', default=''); p.add_argument('--notes', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.catalogue)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    if not a.portal or not a.dataset_name: p.error('--portal and --dataset-name are required unless --list is used')
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
