#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS=['item_id','claim_or_item','source_ref','method','check_result','confidence','reviewer','notes']
METHODS=['source_trace','metadata','location','time','visual','corroboration']

def create(output: Path):
    with output.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
    output.with_suffix('.md').write_text('# Verification Worksheet\n\nUse the CSV to record verification checks by method.\n', encoding='utf-8')
    return {'csv':str(output),'markdown':str(output.with_suffix('.md')),'methods':METHODS}

def audit(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    issues=[]
    for i,r in enumerate(rows,1):
        if not r.get('source_ref'): issues.append({'row':i,'issue':'missing source_ref'})
        if r.get('method') not in METHODS: issues.append({'row':i,'issue':'unknown method'})
    return {'rows':len(rows),'issues':issues,'ok':not issues}

def main():
    p=argparse.ArgumentParser(description='Create or audit a verification worksheet.')
    p.add_argument('--create'); p.add_argument('--audit')
    a=p.parse_args()
    if a.create: print(json.dumps(create(Path(a.create)), indent=2)); return 0
    if not a.audit: p.error('use --create or --audit')
    print(json.dumps(audit(Path(a.audit)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
