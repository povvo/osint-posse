#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sha(p:Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def create(root:Path,out:Path):
    files=[root] if root.is_file() else [p for p in sorted(root.rglob('*')) if p.is_file()]
    rows=[{'path':str(p),'relative':str(p.relative_to(root)) if root.is_dir() else p.name,'sha256':sha(p),'bytes':p.stat().st_size,'checked_utc':now()} for p in files]
    data={'root':str(root),'created_utc':now(),'records':rows}; out.write_text(json.dumps(data,indent=2),encoding='utf-8'); return {'output':str(out),'records':len(rows)}
def verify(manifest:Path):
    data=json.loads(manifest.read_text(encoding='utf-8')); checks=[]
    for r in data.get('records',[]):
        p=Path(r['path']); actual=sha(p) if p.exists() else None; checks.append({'path':str(p),'ok':actual==r.get('sha256'),'expected':r.get('sha256'),'actual':actual})
    return {'checked':len(checks),'ok':all(c['ok'] for c in checks),'checks':checks}
def main():
    p=argparse.ArgumentParser(description='Create or verify digital preservation checksum manifests.')
    sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('create'); c.add_argument('root'); c.add_argument('--output',default='checksum_manifest.json')
    v=sub.add_parser('verify'); v.add_argument('manifest')
    a=p.parse_args(); print(json.dumps(create(Path(a.root),Path(a.output)) if a.cmd=='create' else verify(Path(a.manifest)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
