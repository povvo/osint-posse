#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['tx_id','time','from','to','amount','asset','service','hop','exposure','evidence_ref','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def summarise(p:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    total=0; services={}
    for r in rows:
        try: total+=float(r.get('amount',0) or 0)
        except ValueError: pass
        if r.get('service'): services[r['service']]=services.get(r['service'],0)+1
    return {'rows':len(rows),'total_amount':total,'services':services}
def main():
    ap=argparse.ArgumentParser(description='Create or summarise a crypto payment tracing worksheet.')
    ap.add_argument('--init'); ap.add_argument('--summarise')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.summarise: ap.error('use --init or --summarise')
    print(json.dumps(summarise(Path(a.summarise)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
