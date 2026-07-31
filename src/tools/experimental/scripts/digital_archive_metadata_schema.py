#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
FIELDS=['identifier','title','creator','date','type','format','description','rights','source','coverage','relation']
def init(path: Path):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
    return {'created':str(path),'fields':FIELDS}
def validate(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    findings=[]
    for i,r in enumerate(rows,1):
        for field in ['identifier','title','date','type']:
            if not r.get(field): findings.append({'row':i,'issue':f'missing {field}'})
    return {'rows':len(rows),'ok':not findings,'findings':findings}
def main():
    p=argparse.ArgumentParser(description='Create or validate a digital archive metadata CSV schema.')
    p.add_argument('--init'); p.add_argument('--validate')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)), indent=2)); return 0
    if not a.validate: p.error('use --init or --validate')
    print(json.dumps(validate(Path(a.validate)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
