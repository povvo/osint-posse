#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path

def safe(x):
    s=re.sub(r'[^A-Za-z0-9_]+','_',x.strip().lower()).strip('_')
    return ('c_'+s if s[:1].isdigit() else s) or 'col'
def schema(csv_path:Path,table:str,out:Path):
    with csv_path.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f)); fields=list(rows[0]) if rows else []
    cols=[]
    for field in fields:
        typ='REAL' if field.lower() in {'lat','lon','x','y'} else 'TEXT'
        cols.append(f'  {safe(field)} {typ}')
    sql=f'CREATE TABLE IF NOT EXISTS {safe(table)} (\n'+',\n'.join(cols)+'\n);\n'
    if {'lat','lon'}.issubset({f.lower() for f in fields}): sql+='-- Geometry can be created from lon/lat in a spatial database.\n'
    out.write_text(sql,encoding='utf-8'); return {'output':str(out),'columns':len(fields)}
def main():
    ap=argparse.ArgumentParser(description='Generate SQL schema for spatial attribute tables.')
    ap.add_argument('csv'); ap.add_argument('--table',required=True); ap.add_argument('--output',default='spatial_schema.sql')
    a=ap.parse_args(); print(json.dumps(schema(Path(a.csv),a.table,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
