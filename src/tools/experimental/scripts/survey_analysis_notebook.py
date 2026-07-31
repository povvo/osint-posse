#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def analyse(p:Path,out:Path):
    rows=read(p); fields=list(rows[0]) if rows else []; report={'rows':len(rows),'fields':[]}
    for field in fields:
        vals=[r.get(field,'') for r in rows]; non=[v for v in vals if v!='']; nums=[]
        for v in non:
            try: nums.append(float(v))
            except ValueError: pass
        item={'field':field,'non_empty':len(non),'unique':len(set(non)),'top_values':Counter(non).most_common(5)}
        if nums: item.update({'min':min(nums),'max':max(nums),'mean':statistics.mean(nums)})
        report['fields'].append(item)
    out.write_text(json.dumps(report,indent=2),encoding='utf-8'); return {'output':str(out),'rows':len(rows),'fields':len(fields)}
def main():
    p=argparse.ArgumentParser(description='Profile survey responses and produce a JSON analysis notebook summary.')
    p.add_argument('responses_csv'); p.add_argument('--output',default='survey_analysis.json')
    a=p.parse_args(); print(json.dumps(analyse(Path(a.responses_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
