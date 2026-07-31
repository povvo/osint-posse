#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
FIELDS=['step_id','process','activity','owner','input','output','next_step','control','risk']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def mermaid(p:Path,out:Path):
    with p.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    def sid(x):
        s=re.sub(r'[^A-Za-z0-9_]+','_',x or 'step')
        return 'S_'+s if s[:1].isdigit() else s
    lines=['flowchart TD']
    ids={r.get('step_id','') for r in rows}
    findings=[]
    for r in rows:
        step=r.get('step_id') or r.get('activity') or 'step'
        lines.append(f'  {sid(step)}["{r.get("activity",step)}"]')
        if r.get('next_step'):
            if r['next_step'] not in ids: findings.append({'step':step,'issue':'next_step missing'})
            lines.append(f'  {sid(step)} --> {sid(r["next_step"])}')
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return {'output':str(out),'steps':len(rows),'findings':findings}
def main():
    p=argparse.ArgumentParser(description='Create or render a process map from step records.')
    p.add_argument('--init'); p.add_argument('--input'); p.add_argument('--output',default='process_map.mmd')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.input: p.error('use --init or --input')
    print(json.dumps(mermaid(Path(a.input),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
