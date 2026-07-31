#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def build(p:Path,outdir:Path):
    rows=read(p); flows=defaultdict(float); parties=set()
    for r in rows:
        src=r.get('from') or r.get('source') or ''; dst=r.get('to') or r.get('target') or ''
        try: amt=float(r.get('amount',0) or 0)
        except ValueError: amt=0
        if src and dst: flows[(src,dst)]+=amt; parties.update([src,dst])
    outdir.mkdir(parents=True,exist_ok=True)
    edges=[{'source':a,'target':b,'amount':v} for (a,b),v in flows.items()]
    with (outdir/'flows.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['source','target','amount']); w.writeheader(); w.writerows(edges)
    (outdir/'summary.json').write_text(json.dumps({'parties':len(parties),'flows':len(edges),'total_amount':sum(flows.values())},indent=2),encoding='utf-8')
    return {'output_dir':str(outdir),'parties':len(parties),'flows':len(edges)}
def main():
    ap=argparse.ArgumentParser(description='Build a funds-flow workbook from transaction rows.')
    ap.add_argument('transactions_csv'); ap.add_argument('--output-dir',default='funds_flow')
    a=ap.parse_args(); print(json.dumps(build(Path(a.transactions_csv),Path(a.output_dir)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
