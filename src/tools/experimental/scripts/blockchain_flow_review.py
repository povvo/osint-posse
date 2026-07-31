#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def analyse(p:Path,out:Path):
    rows=read(p); incoming=defaultdict(float); outgoing=defaultdict(float); edges=defaultdict(float)
    for r in rows:
        src=r.get('from') or r.get('source') or ''; dst=r.get('to') or r.get('target') or ''
        try: amt=float(r.get('amount',0) or 0)
        except ValueError: amt=0
        if src and dst: outgoing[src]+=amt; incoming[dst]+=amt; edges[(src,dst)]+=amt
    report={'address_count':len(set(incoming)|set(outgoing)),'edge_count':len(edges),'addresses':[{'address':a,'incoming':incoming[a],'outgoing':outgoing[a],'net':incoming[a]-outgoing[a]} for a in sorted(set(incoming)|set(outgoing))]}
    out.write_text(json.dumps(report,indent=2),encoding='utf-8'); return {'output':str(out),'address_count':report['address_count'],'edge_count':report['edge_count']}
def main():
    ap=argparse.ArgumentParser(description='Summarise blockchain-style value flows from transaction CSV rows.')
    ap.add_argument('transactions_csv'); ap.add_argument('--output',default='blockchain_flow_review.json')
    a=ap.parse_args(); print(json.dumps(analyse(Path(a.transactions_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
