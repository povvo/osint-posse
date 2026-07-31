#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict,deque
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def build(p:Path,root:str):
    rows=read(p); children=defaultdict(list)
    for r in rows: children[r.get('parent','')].append(r)
    tree=[]; q=deque([(root,0)])
    seen=set()
    while q:
        ent,depth=q.popleft()
        if ent in seen: continue
        seen.add(ent); tree.append({'entity':ent,'depth':depth})
        for r in children.get(ent,[]): q.append((r.get('entity',''),depth+1))
    return {'root':root,'nodes':tree,'node_count':len(tree)}
def main():
    ap=argparse.ArgumentParser(description='Build an ownership tree from parent/entity relationship rows.')
    ap.add_argument('relationships_csv'); ap.add_argument('--root',required=True); ap.add_argument('--output',default='ownership_tree.json')
    a=ap.parse_args(); result=build(Path(a.relationships_csv),a.root); Path(a.output).write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps({'output':a.output,'node_count':result['node_count']},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
