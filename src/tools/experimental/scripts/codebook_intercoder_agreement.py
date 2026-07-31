#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path


def read(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def init(path: Path):
    fields=['code','definition','include','exclude','example','reviewer']
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
    return {'created':str(path),'fields':fields}

def agreement(path: Path, item_col: str, coder_col: str, code_col: str):
    rows=read(path); by_item={}
    for r in rows: by_item.setdefault(r.get(item_col,''),[]).append(r)
    results=[]
    for item, vals in by_item.items():
        codes=[v.get(code_col,'') for v in vals if v.get(code_col,'')]
        counts=Counter(codes); total=sum(counts.values())
        agree=max(counts.values())/total if total else 0
        results.append({'item':item,'coder_count':len(vals),'agreement':round(agree,3),'codes':dict(counts)})
    return {'items':len(results),'mean_agreement':round(sum(r['agreement'] for r in results)/len(results),3) if results else 0,'results':results}

def main():
    p=argparse.ArgumentParser(description='Create codebook templates and calculate simple inter-coder agreement.')
    sub=p.add_subparsers(dest='cmd', required=True)
    i=sub.add_parser('init'); i.add_argument('codebook')
    a=sub.add_parser('agreement'); a.add_argument('coded_csv'); a.add_argument('--item-col', default='item_id'); a.add_argument('--coder-col', default='coder'); a.add_argument('--code-col', default='code'); a.add_argument('--output')
    args=p.parse_args()
    if args.cmd=='init': print(json.dumps(init(Path(args.codebook)), indent=2)); return 0
    res=agreement(Path(args.coded_csv), args.item_col, args.coder_col, args.code_col)
    if args.output: Path(args.output).write_text(json.dumps(res, indent=2), encoding='utf-8')
    print(json.dumps(res, indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
