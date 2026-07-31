#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['indicator_id','subject','indicator','proximity','specificity','capability','escalation','protective_action','reviewer','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def score(p:Path,out:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    for r in rows:
        total=0
        for k in ['proximity','specificity','capability','escalation']:
            try: total+=float(r.get(k,0) or 0)
            except ValueError: pass
        r['triage_score']=total; r['priority']='high' if total>=12 else 'medium' if total>=7 else 'low'
    fields=FIELDS+['triage_score','priority']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'rows':len(rows),'high':sum(1 for r in rows if r['priority']=='high')}
def main():
    ap=argparse.ArgumentParser(description='Score protective indicators by proximity, specificity, capability, and escalation.')
    ap.add_argument('--init'); ap.add_argument('--score'); ap.add_argument('--output',default='protective_indicator_scores.csv')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.score: ap.error('use --init or --score')
    print(json.dumps(score(Path(a.score),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
