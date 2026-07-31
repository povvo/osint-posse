#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS=['ir_id','time_utc','priority','requirement','decision_supported','collection_plan','owner','status','due','notes']
STATUSES={'draft','active','satisfied','closed','deferred'}

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
    row={'ir_id':str(uuid.uuid4()),'time_utc':now(),'priority':args.priority,'requirement':args.requirement,'decision_supported':args.decision_supported,'collection_plan':args.collection_plan,'owner':args.owner,'status':'active','due':args.due,'notes':args.notes}
    rows.append(row); write(path, rows); return row

def summary(path: Path):
    rows=read(path)
    return {'total':len(rows),'active':sum(1 for r in rows if r.get('status')=='active'),'by_priority':{p:sum(1 for r in rows if r.get('priority')==p) for p in sorted({r.get('priority','') for r in rows})}}

def main():
    p=argparse.ArgumentParser(description='Define and track intelligence requirements and collection plans.')
    sub=p.add_subparsers(dest='cmd', required=True)
    a=sub.add_parser('add'); a.add_argument('register'); a.add_argument('--priority', default='normal'); a.add_argument('--requirement', required=True); a.add_argument('--decision-supported', default=''); a.add_argument('--collection-plan', default=''); a.add_argument('--owner', default=''); a.add_argument('--due', default=''); a.add_argument('--notes', default='')
    s=sub.add_parser('summary'); s.add_argument('register')
    l=sub.add_parser('list'); l.add_argument('register')
    args=p.parse_args()
    if args.cmd=='add': print(json.dumps(add(Path(args.register), args), indent=2)); return 0
    if args.cmd=='summary': print(json.dumps(summary(Path(args.register)), indent=2)); return 0
    print(json.dumps(read(Path(args.register)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
