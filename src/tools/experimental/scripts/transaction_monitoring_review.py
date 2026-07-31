#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
RULES={'round_amount':lambda r: str(r.get('amount','')).endswith('000'),'high_value':lambda r: abs(float(r.get('amount',0) or 0))>=10000,'missing_counterparty':lambda r: not r.get('counterparty')}
def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def review(p:Path,out:Path):
    rows=read(p); alerts=[]
    for i,r in enumerate(rows,1):
        hits=[]
        for name,fn in RULES.items():
            try:
                if fn(r): hits.append(name)
            except Exception: pass
        if hits: alerts.append({'row':i,'hits':';'.join(hits),'transaction':r})
    out.write_text(json.dumps({'alerts':alerts,'alert_count':len(alerts)},indent=2),encoding='utf-8'); return {'output':str(out),'alert_count':len(alerts)}
def main():
    ap=argparse.ArgumentParser(description='Review transaction CSV rows for simple alert patterns.')
    ap.add_argument('transactions_csv'); ap.add_argument('--output',default='transaction_alerts.json')
    a=ap.parse_args(); print(json.dumps(review(Path(a.transactions_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
