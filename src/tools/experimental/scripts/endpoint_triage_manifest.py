#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['path','bytes','sha256','category','collected_utc','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def manifest(root:Path,out:Path,category:str):
    files=[root] if root.is_file() else [p for p in sorted(root.rglob('*')) if p.is_file()]
    rows=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'category':category,'collected_utc':now(),'notes':''} for p in files]
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'records':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Create an endpoint triage artefact manifest from local files.')
    ap.add_argument('root'); ap.add_argument('--category',default='triage'); ap.add_argument('--output',default='endpoint_triage_manifest.csv')
    a=ap.parse_args(); print(json.dumps(manifest(Path(a.root),Path(a.output),a.category),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
