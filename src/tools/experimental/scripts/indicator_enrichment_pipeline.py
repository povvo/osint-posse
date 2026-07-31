#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def enrich(p:Path,out:Path):
    rows=read(p); enriched=[]
    for r in rows:
        val=r.get('indicator') or r.get('value') or ''
        typ=r.get('indicator_type') or ('ip' if val.count('.')==3 and all(x.isdigit() for x in val.split('.')) else 'domain' if '.' in val else 'other')
        enriched.append({**r,'normalised_indicator':val.lower().strip(),'inferred_type':typ,'needs_dns_review':'yes' if typ in {'domain','ip'} else 'no','needs_file_review':'yes' if typ in {'hash','file'} else 'no','enrichment_status':'queued'})
    fields=sorted({k for r in enriched for k in r}) if enriched else ['normalised_indicator']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(enriched)
    return {'output':str(out),'rows':len(enriched)}
def main():
    ap=argparse.ArgumentParser(description='Normalise indicator CSV rows and queue enrichment review fields.')
    ap.add_argument('indicators_csv'); ap.add_argument('--output',default='indicator_enrichment_queue.csv')
    a=ap.parse_args(); print(json.dumps(enrich(Path(a.indicators_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
