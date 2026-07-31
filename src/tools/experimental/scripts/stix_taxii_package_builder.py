#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def bundle(p:Path,out:Path):
    rows=read(p); objects=[]
    for r in rows:
        value=r.get('value') or r.get('indicator') or ''
        typ=r.get('type') or r.get('object_type') or 'indicator'
        objects.append({'type':typ,'id':f'{typ}--{uuid.uuid4()}','created':now(),'modified':now(),'name':value,'description':r.get('description',''),'labels':[r.get('label','manual')]})
    data={'type':'bundle','id':f'bundle--{uuid.uuid4()}','objects':objects}
    out.write_text(json.dumps(data,indent=2),encoding='utf-8'); return {'output':str(out),'objects':len(objects)}
def main():
    ap=argparse.ArgumentParser(description='Build a local STIX-style JSON bundle from indicator/object CSV rows.')
    ap.add_argument('objects_csv'); ap.add_argument('--output',default='stix_bundle.json')
    a=ap.parse_args(); print(json.dumps(bundle(Path(a.objects_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
