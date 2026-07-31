#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['stakeholder_id','name','type','influence','interest','relationship','needs','risks','engagement_action']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def analyse(p:Path,out:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    for r in rows:
        try: score=float(r.get('influence',0) or 0)*float(r.get('interest',0) or 0)
        except ValueError: score=0
        r['priority_score']=score
    rows.sort(key=lambda r:float(r.get('priority_score',0)), reverse=True)
    fields=FIELDS+['priority_score']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'stakeholders':len(rows),'top':rows[:5]}
def main():
    p=argparse.ArgumentParser(description='Create or score a stakeholder map.')
    p.add_argument('--init'); p.add_argument('--analyse'); p.add_argument('--output',default='stakeholder_map_scored.csv')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.analyse: p.error('use --init or --analyse')
    print(json.dumps(analyse(Path(a.analyse),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
