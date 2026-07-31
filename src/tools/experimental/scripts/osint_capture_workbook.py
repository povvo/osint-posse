#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['capture_id','time_utc','query','locator','capture_file','sha256','source_type','status','verification_note','next_action']
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
    rows=read(p); row={'capture_id':str(uuid.uuid4()),'time_utc':now(),'query':a.query,'locator':a.locator,'capture_file':a.capture_file,'sha256':digest(Path(a.capture_file)),'source_type':a.source_type,'status':a.status,'verification_note':a.verification_note,'next_action':a.next_action}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Maintain an OSINT capture workbook for queries, files, and verification notes.')
    ap.add_argument('workbook'); ap.add_argument('--query',required=True); ap.add_argument('--locator',default=''); ap.add_argument('--capture-file',default=''); ap.add_argument('--source-type',default='web'); ap.add_argument('--status',default='captured'); ap.add_argument('--verification-note',default=''); ap.add_argument('--next-action',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.workbook)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
