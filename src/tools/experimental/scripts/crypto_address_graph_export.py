#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def export(p:Path,outdir:Path):
    rows=read(p); nodes={}; edges=[]
    for r in rows:
        s=r.get('from') or r.get('source') or ''; t=r.get('to') or r.get('target') or ''
        if not s or not t: continue
        nodes.setdefault(s,{'id':s,'label':s,'kind':r.get('source_kind','address')}); nodes.setdefault(t,{'id':t,'label':t,'kind':r.get('target_kind','address')})
        edges.append({'source':s,'target':t,'amount':r.get('amount',''),'reference':r.get('source_ref','')})
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/'nodes.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['id','label','kind']); w.writeheader(); w.writerows(nodes.values())
    with (outdir/'edges.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['source','target','amount','reference']); w.writeheader(); w.writerows(edges)
    return {'output_dir':str(outdir),'nodes':len(nodes),'edges':len(edges)}
def main():
    ap=argparse.ArgumentParser(description='Export address/entity relationships into node and edge CSVs.')
    ap.add_argument('transactions_csv'); ap.add_argument('--output-dir',default='crypto_address_graph')
    a=ap.parse_args(); print(json.dumps(export(Path(a.transactions_csv),Path(a.output_dir)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
