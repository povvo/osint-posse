#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
CHECKS=['identity','ownership','control','business_activity','jurisdiction','source_of_funds','screening','adverse_media','documents','approval']
def create(out:Path,subject:str):
    fields=['check','subject','status','reference','result','reviewer','notes']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows([{'check':c,'subject':subject,'status':'pending','reference':'','result':'','reviewer':'','notes':''} for c in CHECKS])
    return {'output':str(out),'checks':len(CHECKS)}
def audit(p:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    issues=[]
    for i,r in enumerate(rows,1):
        if r.get('status')!='complete': issues.append({'row':i,'check':r.get('check'),'issue':'not complete'})
        if not r.get('reference'): issues.append({'row':i,'check':r.get('check'),'issue':'missing reference'})
    return {'rows':len(rows),'ready':not issues,'issues':issues}
def main():
    ap=argparse.ArgumentParser(description='Create or audit a due-diligence checklist.')
    ap.add_argument('--create'); ap.add_argument('--subject',default=''); ap.add_argument('--audit')
    a=ap.parse_args()
    if a.create: print(json.dumps(create(Path(a.create),a.subject),indent=2)); return 0
    if not a.audit: ap.error('use --create or --audit')
    print(json.dumps(audit(Path(a.audit)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
