#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['rule_file','rule_type','sha256','status','version','owner','test_result','notes']
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def index(root:Path,out:Path):
    rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.suffix.lower() in {'.yar','.yara','.yml','.yaml','.sigma'}:
            typ='yara' if p.suffix.lower() in {'.yar','.yara'} else 'sigma'
            rows.append({'rule_file':str(p),'rule_type':typ,'sha256':sha(p),'status':'active','version':'','owner':'','test_result':'not_run','notes':''})
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'rules':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Index and version local detection rule files.')
    ap.add_argument('rules_root'); ap.add_argument('--output',default='detection_rule_repository.csv')
    a=ap.parse_args(); print(json.dumps(index(Path(a.rules_root),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
