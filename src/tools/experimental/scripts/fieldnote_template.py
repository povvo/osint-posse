#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS=['note_id','time_utc','observer','place','activity','observation','context','reflection','codes','follow_up']

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def read(path: Path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def write(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path: Path, args):
    rows=read(path)
    row={'note_id':str(uuid.uuid4()),'time_utc':now(),'observer':args.observer,'place':args.place,'activity':args.activity,'observation':args.observation,'context':args.context,'reflection':args.reflection,'codes':';'.join(args.code or []),'follow_up':args.follow_up}
    rows.append(row); write(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Capture field observations with context, reflection, codes, and follow-up actions.')
    p.add_argument('notes'); p.add_argument('--observer', default=''); p.add_argument('--place', default=''); p.add_argument('--activity', default=''); p.add_argument('--observation'); p.add_argument('--context', default=''); p.add_argument('--reflection', default=''); p.add_argument('--code', action='append'); p.add_argument('--follow-up', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.notes)
    if a.list: print(json.dumps(read(path), indent=2, ensure_ascii=False)); return 0
    if not a.observation: p.error('--observation is required unless --list is used')
    print(json.dumps(add(path,a), indent=2, ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
