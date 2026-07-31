#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def priority(row):
    total=0
    for field in ['value','urgency','feasibility','risk_reduction']:
        try: total+=float(row.get(field,0) or 0)
        except ValueError: pass
    return total
def rank(infile:Path,outfile:Path):
    rows=read(infile)
    for r in rows: r['priority_score']=priority(r)
    rows.sort(key=lambda r: float(r['priority_score']), reverse=True)
    fields=sorted({k for r in rows for k in r}) if rows else ['priority_score']
    with outfile.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(outfile),'rows':len(rows),'top':rows[:5]}
def main():
    p=argparse.ArgumentParser(description='Prioritise lines of enquiry by value, urgency, feasibility, and risk reduction.')
    p.add_argument('input_csv'); p.add_argument('--output',default='prioritised_enquiries.csv')
    a=p.parse_args(); print(json.dumps(rank(Path(a.input_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
