#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict,deque
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def hops(rows,start,max_hops):
    adj=defaultdict(list)
    for r in rows:
        s=r.get('from') or r.get('source'); t=r.get('to') or r.get('target')
        if s and t: adj[s].append((t,r))
    seen={start}; q=deque([(start,0)]); reached=[]
    while q:
        node,depth=q.popleft(); reached.append({'address':node,'hop':depth})
        if depth>=max_hops: continue
        for nxt,_ in adj.get(node,[]):
            if nxt not in seen: seen.add(nxt); q.append((nxt,depth+1))
    return reached
def analyse(p:Path,start:str,max_hops:int,out:Path):
    rows=read(p); result={'start':start,'max_hops':max_hops,'reached':hops(rows,start,max_hops)}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),'reached':len(result['reached'])}
def main():
    ap=argparse.ArgumentParser(description='Trace simple on-chain hops from transaction CSV rows.')
    ap.add_argument('transactions_csv'); ap.add_argument('--start',required=True); ap.add_argument('--max-hops',type=int,default=3); ap.add_argument('--output',default='onchain_flow_notebook.json')
    a=ap.parse_args(); print(json.dumps(analyse(Path(a.transactions_csv),a.start,a.max_hops,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
