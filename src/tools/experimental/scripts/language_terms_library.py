#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

FIELDS=['term','language','meaning','context','reference','confidence','notes']

def read(path: Path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def save(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path: Path, args):
    rows=read(path); row={field:getattr(args, field) for field in FIELDS}
    rows.append(row); save(path, rows); return row

def find(path: Path, pattern: str):
    rx=re.compile(pattern, re.I)
    return [r for r in read(path) if rx.search(' '.join(str(v) for v in r.values()))]

def main():
    p=argparse.ArgumentParser(description='Maintain a multilingual terminology reference library.')
    sub=p.add_subparsers(dest='cmd', required=True)
    a=sub.add_parser('add'); a.add_argument('library')
    for field in FIELDS: a.add_argument('--'+field.replace('_','-'), default='')
    s=sub.add_parser('search'); s.add_argument('library'); s.add_argument('pattern')
    l=sub.add_parser('list'); l.add_argument('library')
    args=p.parse_args()
    if args.cmd=='add': print(json.dumps(add(Path(args.library), args), indent=2, ensure_ascii=False)); return 0
    if args.cmd=='search': print(json.dumps(find(Path(args.library), args.pattern), indent=2, ensure_ascii=False)); return 0
    print(json.dumps(read(Path(args.library)), indent=2, ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
