#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['review_id','time_utc','sample_file','sha256','tool','file_type','strings_note','imports_note','risk_note','reviewer','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def digest(p):
    if not p.exists() or not p.is_file(): return ''
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'review_id':str(uuid.uuid4()),'time_utc':now(),'sample_file':a.sample_file,'sha256':digest(Path(a.sample_file)),'tool':a.tool,'file_type':a.file_type,'strings_note':a.strings_note,'imports_note':a.imports_note,'risk_note':a.risk_note,'reviewer':a.reviewer,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record static review notes for local binary samples and supporting files.')
    ap.add_argument('log'); ap.add_argument('--sample-file',required=True); ap.add_argument('--tool',default='manual'); ap.add_argument('--file-type',default='unknown'); ap.add_argument('--strings-note',default=''); ap.add_argument('--imports-note',default=''); ap.add_argument('--risk-note',default=''); ap.add_argument('--reviewer',default=''); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
