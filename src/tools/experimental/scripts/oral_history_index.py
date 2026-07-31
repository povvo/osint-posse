#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
FIELDS=['id','name','file','text','summary','note']
def read(p):
    if not p.exists(): return []
    with p.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def main():
    ap=argparse.ArgumentParser(description='Maintain a simple oral history index.')
    ap.add_argument('csv'); ap.add_argument('--name'); ap.add_argument('--file', default=''); ap.add_argument('--text', default=''); ap.add_argument('--summary', default=''); ap.add_argument('--note', default=''); ap.add_argument('--list', action='store_true')
    a=ap.parse_args(); p=Path(a.csv)
    if a.list: print(json.dumps(read(p), indent=2)); return 0
    rows=read(p); row={'id':str(len(rows)+1),'name':a.name or '', 'file':a.file, 'text':a.text, 'summary':a.summary, 'note':a.note}; rows.append(row); save(p, rows); print(json.dumps(row, indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
