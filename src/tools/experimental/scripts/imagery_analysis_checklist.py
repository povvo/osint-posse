#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['image_id','source','sensor','capture_date','location','geolocation_basis','interpretation','confidence','limitations','reviewer','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def audit(p:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    issues=[]
    for i,r in enumerate(rows,1):
        for field in ['source','capture_date','location','interpretation','confidence']:
            if not r.get(field): issues.append({'row':i,'issue':f'missing {field}'})
    return {'rows':len(rows),'ready':not issues,'issues':issues}
def main():
    ap=argparse.ArgumentParser(description='Create or audit an imagery analysis checklist.')
    ap.add_argument('--init'); ap.add_argument('--audit')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.audit: ap.error('use --init or --audit')
    print(json.dumps(audit(Path(a.audit)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
