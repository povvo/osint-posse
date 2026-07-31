#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def run(input_csv:Path,outdir:Path,a_col:str,b_col:str):
    with input_csv.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    items={}; pairs=[]
    for r in rows:
        a=r.get(a_col,''); b=r.get(b_col,'')
        if not a or not b: continue
        items.setdefault(a,{'id':a,'label':a}); items.setdefault(b,{'id':b,'label':b}); pairs.append({'from':a,'to':b,'kind':r.get('relationship','related')})
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/'items.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['id','label']); w.writeheader(); w.writerows(items.values())
    with (outdir/'pairs.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['from','to','kind']); w.writeheader(); w.writerows(pairs)
    return {'output_dir':str(outdir),'items':len(items),'pairs':len(pairs)}
def main():
    ap=argparse.ArgumentParser(description='Split a pair table into item and pair CSV outputs.')
    ap.add_argument('input_csv'); ap.add_argument('--output-dir',default='chart_edges_export'); ap.add_argument('--a-col',default='source'); ap.add_argument('--b-col',default='target')
    a=ap.parse_args(); print(json.dumps(run(Path(a.input_csv),Path(a.output_dir),a.a_col,a.b_col),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
