#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,shutil,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['capture_id','time_utc','locator','source_file','archive_file','sha256','source_type','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def add(log:Path,source:Path,archive_dir:Path,locator:str,source_type:str,notes:str):
    archive_dir.mkdir(parents=True,exist_ok=True); target=archive_dir/(uuid.uuid4().hex+'_'+source.name); shutil.copy2(source,target)
    row={'capture_id':str(uuid.uuid4()),'time_utc':now(),'locator':locator,'source_file':str(source),'archive_file':str(target),'sha256':digest(target),'source_type':source_type,'notes':notes}
    rows=[]
    if log.exists():
        with log.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    rows.append(row)
    with log.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return row
def main():
    ap=argparse.ArgumentParser(description='Archive local captured content files and record hashes and locators.')
    ap.add_argument('log'); ap.add_argument('source_file'); ap.add_argument('--archive-dir',default='content_archive'); ap.add_argument('--locator',default=''); ap.add_argument('--source-type',default='web'); ap.add_argument('--notes',default='')
    a=ap.parse_args(); print(json.dumps(add(Path(a.log),Path(a.source_file),Path(a.archive_dir),a.locator,a.source_type,a.notes),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
