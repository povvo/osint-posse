#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
FIELDS=['entity','parent','relationship','ownership_percent','jurisdiction','source_ref','notes']
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
        ent=r.get('entity',''); par=r.get('parent','')
        if ent: lines.append(f'  {sid(ent)}["{ent}"]')
        if par: lines.append(f'  {sid(par)} -->|{r.get("relationship","owns")} {r.get("ownership_percent","")}| {sid(ent)}')
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return {'output':str(out),'relationships':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Create or render a corporate structure chart from relationship rows.')
    ap.add_argument('--init'); ap.add_argument('--input'); ap.add_argument('--output',default='corporate_structure.mmd')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.input: ap.error('use --init or --input')
    print(json.dumps(render(Path(a.input),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
