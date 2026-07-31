#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,os
from pathlib import Path
FIELDS=['path','type','bytes','modified','finding','source_ref','notes']
def walk(root:Path,out:Path):
    rows=[]
    for p in sorted(root.rglob('*')):
        try: st=p.stat(); rows.append({'path':str(p),'type':'dir' if p.is_dir() else 'file','bytes':st.st_size if p.is_file() else 0,'modified':st.st_mtime,'finding':'','source_ref':'','notes':''})
        except OSError as e: rows.append({'path':str(p),'type':'error','bytes':'','modified':'','finding':str(e),'source_ref':'','notes':''})
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'items':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Create a file-system review inventory from a local folder.')
    ap.add_argument('root'); ap.add_argument('--output',default='file_system_review.csv')
    a=ap.parse_args(); print(json.dumps(walk(Path(a.root),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
