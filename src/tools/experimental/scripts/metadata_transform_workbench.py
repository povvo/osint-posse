#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path

def change(value,mode):
    if mode=='sha256': return hashlib.sha256(value.encode('utf-8')).hexdigest()
    if mode=='lower': return value.lower()
    if mode=='upper': return value.upper()
    if mode=='strip': return value.strip()
    raise ValueError('unknown mode')
def process(input_csv:Path,out:Path,column:str,mode:str):
    with input_csv.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f)); fields=list(rows[0]) if rows else []
    new=f'{column}_{mode}'; fields.append(new)
    for r in rows: r[new]=change(r.get(column,''),mode)
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'rows':len(rows),'mode':mode}
def main():
    ap=argparse.ArgumentParser(description='Apply local text cleanup or hash transforms to a CSV column.')
    ap.add_argument('input_csv'); ap.add_argument('--column',required=True); ap.add_argument('--mode',choices=['sha256','lower','upper','strip'],required=True); ap.add_argument('--output',default='metadata_transform.csv')
    a=ap.parse_args(); print(json.dumps(process(Path(a.input_csv),Path(a.output),a.column,a.mode),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
