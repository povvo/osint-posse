#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['reference','title','date','level','extent','creator','scope_content','arrangement','access_note']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def validate(p:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    issues=[]
    for i,r in enumerate(rows,1):
        for field in ['reference','title','level']:
            if not r.get(field): issues.append({'row':i,'issue':f'missing {field}'})
    return {'rows':len(rows),'ok':not issues,'issues':issues}
def main():
    ap=argparse.ArgumentParser(description='Create or validate an archival catalogue CSV.')
    ap.add_argument('--init'); ap.add_argument('--validate')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.validate: ap.error('use --init or --validate')
    print(json.dumps(validate(Path(a.validate)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
