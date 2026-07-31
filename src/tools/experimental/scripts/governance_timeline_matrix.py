#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['date','decision','body','policy','actor','source_ref','impact','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def build(csv_path:Path,out:Path):
    with csv_path.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    rows.sort(key=lambda r:r.get('date',''))
    lines=['# Governance Timeline','']
    for r in rows: lines.append(f"- **{r.get('date','undated')}** — {r.get('decision','')} · {r.get('body','')} [{r.get('source_ref','')}]")
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return {'output':str(out),'events':len(rows)}
def main():
    p=argparse.ArgumentParser(description='Create or render a governance timeline matrix.')
    p.add_argument('--init'); p.add_argument('--input'); p.add_argument('--output',default='governance_timeline.md')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.input: p.error('use --init or --input')
    print(json.dumps(build(Path(a.input),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
