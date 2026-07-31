#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from pathlib import Path
FIELDS=['question_id','section','question','response_type','required','options','notes']
def init(path:Path):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(path),'fields':FIELDS}
def add(path:Path,args):
    rows=[]
    if path.exists():
        with path.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    row={'question_id':str(uuid.uuid4()),'section':args.section,'question':args.question,'response_type':args.response_type,'required':args.required,'options':';'.join(args.option or []),'notes':args.notes}
    rows.append(row)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return row
def main():
    p=argparse.ArgumentParser(description='Create and maintain a structured survey questionnaire CSV.')
    sub=p.add_subparsers(dest='cmd',required=True)
    i=sub.add_parser('init'); i.add_argument('survey')
    a=sub.add_parser('add'); a.add_argument('survey'); a.add_argument('--section',default='main'); a.add_argument('--question',required=True); a.add_argument('--response-type',default='text'); a.add_argument('--required',default='yes'); a.add_argument('--option',action='append'); a.add_argument('--notes',default='')
    args=p.parse_args(); print(json.dumps(init(Path(args.survey)) if args.cmd=='init' else add(Path(args.survey),args),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
