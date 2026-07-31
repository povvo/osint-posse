#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['competitor','product','market','capability','partnership','signal','source_ref','score','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def summary(p:Path,out:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    totals={}
    for r in rows:
        try: score=float(r.get('score',0) or 0)
        except ValueError: score=0
        totals[r.get('competitor','unknown')]=totals.get(r.get('competitor','unknown'),0)+score
    result={'competitors':len(totals),'scores':totals,'top':sorted(totals.items(),key=lambda x:x[1],reverse=True)[:10]}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),**result}
def main():
    ap=argparse.ArgumentParser(description='Create or summarise a competitor landscape matrix.')
    ap.add_argument('--init'); ap.add_argument('--summarise'); ap.add_argument('--output',default='competitor_landscape.json')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.summarise: ap.error('use --init or --summarise')
    print(json.dumps(summary(Path(a.summarise),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
