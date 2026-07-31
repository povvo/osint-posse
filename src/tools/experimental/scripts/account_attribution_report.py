#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['indicator','value','source_ref','strength','caveat','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def build(p:Path,out:Path,account:str):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    score=0; caveats=[]
    for r in rows:
        try: score+=float(r.get('strength',0) or 0)
        except ValueError: pass
        if r.get('caveat'): caveats.append(r['caveat'])
    report={'account':account,'indicator_count':len(rows),'support_score':score,'caveats':caveats,'confidence':'high' if score>=10 else 'medium' if score>=5 else 'low','indicators':rows}
    out.write_text(json.dumps(report,indent=2),encoding='utf-8'); return {'output':str(out),'confidence':report['confidence'],'indicator_count':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Create or build a public account attribution evidence report.')
    ap.add_argument('--init'); ap.add_argument('--indicators'); ap.add_argument('--account',default=''); ap.add_argument('--output',default='account_attribution_report.json')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.indicators: ap.error('use --init or --indicators')
    print(json.dumps(build(Path(a.indicators),Path(a.output),a.account),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
