#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
WEIGHTS={'jurisdiction_risk':3,'ownership_complexity':2,'activity_risk':2,'alert_count':1,'screening_hit':4}
def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def score(p:Path,out:Path):
    rows=read(p)
    for r in rows:
        total=0
        for field,weight in WEIGHTS.items():
            try: total+=float(r.get(field,0) or 0)*weight
            except ValueError: pass
        r['risk_score']=total; r['risk_band']='high' if total>=20 else 'medium' if total>=10 else 'low'
    fields=sorted({k for r in rows for k in r}) if rows else ['risk_score']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'rows':len(rows),'high':sum(1 for r in rows if r.get('risk_band')=='high')}
def main():
    ap=argparse.ArgumentParser(description='Score customer or entity risk from jurisdiction, ownership, activity, alerts, and screening fields.')
    ap.add_argument('input_csv'); ap.add_argument('--output',default='customer_risk_scores.csv')
    a=ap.parse_args(); print(json.dumps(score(Path(a.input_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
