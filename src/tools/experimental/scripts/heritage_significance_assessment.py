#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['asset_id','name','fabric','context','condition','rarity','historical_value','community_value','risk','significance','recommendation']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def score(p:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    out=[]
    for r in rows:
        vals=[]
        for k in ['rarity','historical_value','community_value','risk']:
            try: vals.append(float(r.get(k,0) or 0))
            except ValueError: vals.append(0)
        r['significance_score']=sum(vals[:3])-vals[3]; out.append(r)
    return {'rows':len(out),'assets':out}
def main():
    ap=argparse.ArgumentParser(description='Create or score a heritage significance assessment table.')
    ap.add_argument('--init'); ap.add_argument('--score')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.score: ap.error('use --init or --score')
    print(json.dumps(score(Path(a.score)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
