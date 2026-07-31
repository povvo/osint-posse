#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
AMOUNT=re.compile(r'-?\d+(?:\.\d{2})?')
def parse_text(p:Path):
    rows=[]
    for i,line in enumerate(p.read_text(encoding='utf-8',errors='replace').splitlines(),1):
        amounts=AMOUNT.findall(line)
        if amounts: rows.append({'line':i,'date':line[:10] if len(line)>=10 else '','description':line,'amount':amounts[-1]})
    return rows
def convert(inp:Path,out:Path):
    if inp.suffix.lower()=='.csv':
        with inp.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    else: rows=parse_text(inp)
    fields=sorted({k for r in rows for k in r}) if rows else ['date','description','amount']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'rows':len(rows)}
def main():
    ap=argparse.ArgumentParser(description='Convert statement or ledger text into structured transaction rows.')
    ap.add_argument('input_file'); ap.add_argument('--output',default='parsed_transactions.csv')
    a=ap.parse_args(); print(json.dumps(convert(Path(a.input_file),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
