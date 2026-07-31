#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def compare(before:Path,after:Path,id_col:str,out:Path):
    a={r.get(id_col):r for r in read(before) if r.get(id_col)}; b={r.get(id_col):r for r in read(after) if r.get(id_col)}
    added=sorted(k for k in b if k not in a); removed=sorted(k for k in a if k not in b); changed=[]
    for k in sorted(a.keys() & b.keys()):
        diffs={f:{'before':a[k].get(f,''),'after':b[k].get(f,'')} for f in set(a[k])|set(b[k]) if a[k].get(f,'')!=b[k].get(f,'')}
        if diffs: changed.append({'id':k,'changes':diffs})
    result={'added':added,'removed':removed,'changed':changed,'added_count':len(added),'removed_count':len(removed),'changed_count':len(changed)}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),**{k:result[k] for k in ['added_count','removed_count','changed_count']}}
def main():
    ap=argparse.ArgumentParser(description='Compare before/after feature tables and report changes.')
    ap.add_argument('before_csv'); ap.add_argument('after_csv'); ap.add_argument('--id-col',default='id'); ap.add_argument('--output',default='change_detection.json')
    a=ap.parse_args(); print(json.dumps(compare(Path(a.before_csv),Path(a.after_csv),a.id_col,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
