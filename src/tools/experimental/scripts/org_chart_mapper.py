#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
FIELDS=['role','parent_role','authority','next_role','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def render(p:Path,out:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    def sid(x):
        s=re.sub(r'[^A-Za-z0-9_]+','_',x or 'node'); return 'N_'+s if s[:1].isdigit() else s
    lines=['flowchart TD']
    for r in rows:
        role=r.get('role','')
        if role: lines.append(f'  {sid(role)}["{role}"]')
        if r.get('parent_role'): lines.append(f'  {sid(role)} --> {sid(r["parent_role"])}')
        if r.get('next_role'): lines.append(f'  {sid(role)} -.-> {sid(r["next_role"])}')
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return {'output':str(out),'rows':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Create or render an organisation chart table.')
    ap.add_argument('--init'); ap.add_argument('--input'); ap.add_argument('--output',default='org_chart.mmd')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.input: ap.error('use --init or --input')
    print(json.dumps(render(Path(a.input),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
