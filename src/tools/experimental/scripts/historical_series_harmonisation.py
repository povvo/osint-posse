#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def harmonise(input_csv: Path, output_csv: Path, value_col: str, factor_col: str):
    rows=read(input_csv); out=[]
    for r in rows:
        try: value=float(r.get(value_col,0) or 0); factor=float(r.get(factor_col,1) or 1)
        except ValueError: value=0; factor=1
        r['harmonised_value']=value*factor
        r['harmonisation_note']=f'{value_col} multiplied by {factor_col}'
        out.append(r)
    fields=sorted({k for r in out for k in r}) if out else ['harmonised_value']
    with output_csv.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction='ignore'); w.writeheader(); w.writerows(out)
    return {'output':str(output_csv),'rows':len(out)}

def main():
    p=argparse.ArgumentParser(description='Harmonise historical series using a supplied factor column.')
    p.add_argument('input_csv'); p.add_argument('--value-col', required=True); p.add_argument('--factor-col', required=True); p.add_argument('--output', default='harmonised_series.csv')
    a=p.parse_args(); print(json.dumps(harmonise(Path(a.input_csv), Path(a.output), a.value_col, a.factor_col), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
