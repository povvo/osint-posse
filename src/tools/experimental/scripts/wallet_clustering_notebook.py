#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def cluster(p:Path,key_col:str,out:Path):
    rows=read(p); groups=defaultdict(set)
    for r in rows:
        key=r.get(key_col) or r.get('cluster') or 'unassigned'
        for field in ['from','to','source','target','address']:
            if r.get(field): groups[key].add(r[field])
    result={'cluster_count':len(groups),'clusters':[{'cluster':k,'addresses':sorted(v),'size':len(v)} for k,v in sorted(groups.items())]}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),'cluster_count':len(groups)}
def main():
    ap=argparse.ArgumentParser(description='Cluster wallet/address rows using a declared evidence key.')
    ap.add_argument('input_csv'); ap.add_argument('--key-col',default='cluster_key'); ap.add_argument('--output',default='wallet_clusters.json')
    a=ap.parse_args(); print(json.dumps(cluster(Path(a.input_csv),a.key_col,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
