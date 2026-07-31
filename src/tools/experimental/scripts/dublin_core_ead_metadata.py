#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
DC=['identifier','title','creator','subject','description','publisher','contributor','date','type','format','source','language','relation','coverage','rights']
EAD=['ead_id','collection_title','unit_id','unit_date','extent','repository','scope_content','arrangement','access_restrictions']
def init(path:Path, kind:str):
    fields=DC if kind=='dc' else EAD
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    return {'created':str(path),'kind':kind,'fields':fields}
def validate(path:Path, kind:str):
    fields=DC if kind=='dc' else EAD
    required=['identifier','title','date'] if kind=='dc' else ['ead_id','collection_title','unit_id']
    with path.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    findings=[]
    for i,r in enumerate(rows,1):
        for field in required:
            if not r.get(field): findings.append({'row':i,'issue':f'missing {field}'})
    return {'rows':len(rows),'kind':kind,'ok':not findings,'findings':findings}
def main():
    ap=argparse.ArgumentParser(description='Create or validate Dublin Core / EAD metadata CSV files.')
    ap.add_argument('--init'); ap.add_argument('--validate'); ap.add_argument('--kind',choices=['dc','ead'],default='dc')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init),a.kind),indent=2)); return 0
    if not a.validate: ap.error('use --init or --validate')
    print(json.dumps(validate(Path(a.validate),a.kind),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
