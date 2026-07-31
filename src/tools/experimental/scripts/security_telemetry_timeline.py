#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['time','host','source','event_type','severity','summary','action','owner','notes']
def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def build(p:Path,out:Path):
    rows=read(p); rows.sort(key=lambda r:r.get('time',''))
    lines=['# Security Telemetry Timeline','']
    for r in rows: lines.append(f"- **{r.get('time','')}** {r.get('host','')} {r.get('event_type','')} {r.get('summary','')} [{r.get('severity','')}]" )
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8'); return {'output':str(out),'events':len(rows)}
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def main():
    ap=argparse.ArgumentParser(description='Create or render a security telemetry timeline.')
    ap.add_argument('--init'); ap.add_argument('--input'); ap.add_argument('--output',default='security_telemetry_timeline.md')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.input: ap.error('use --init or --input')
    print(json.dumps(build(Path(a.input),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
