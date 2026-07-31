#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['time','phase','system','event','evidence_ref','action','owner','status','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def render(p:Path,out:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    rows.sort(key=lambda r:r.get('time',''))
    lines=['# Incident Timeline','']
    for r in rows: lines.append(f"- **{r.get('time','')}** {r.get('phase','')} {r.get('system','')} — {r.get('event','')} ({r.get('status','')})")
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8'); return {'output':str(out),'events':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Create or render an incident response timeline workbook.')
    ap.add_argument('--init'); ap.add_argument('--input'); ap.add_argument('--output',default='incident_timeline.md')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.input: ap.error('use --init or --input')
    print(json.dumps(render(Path(a.input),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
