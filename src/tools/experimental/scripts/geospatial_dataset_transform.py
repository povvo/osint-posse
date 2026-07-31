#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def transform(p:Path,out:Path,keep:list[str],rename:list[str]):
    rows=read(p); mapping={}
    for item in rename:
        if '=' in item:
            old,new=item.split('=',1); mapping[old]=new
    outrows=[]
    for r in rows:
        item={mapping.get(k,k):v for k,v in r.items() if not keep or k in keep}
        outrows.append(item)
    fields=sorted({k for r in outrows for k in r}) if outrows else []
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(outrows)
    return {'output':str(out),'rows':len(outrows),'fields':fields}
def main():
    ap=argparse.ArgumentParser(description='Clean and transform geospatial attribute CSV rows.')
    ap.add_argument('input_csv'); ap.add_argument('--keep',action='append',default=[]); ap.add_argument('--rename',action='append',default=[]); ap.add_argument('--output',default='geospatial_transform.csv')
    a=ap.parse_args(); print(json.dumps(transform(Path(a.input_csv),Path(a.output),a.keep,a.rename),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
