#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,uuid
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['enrich_id','time_utc','indicator','indicator_type','dns_note','whois_note','certificate_note','hosting_note','source_ref','confidence','notes']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def save(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def add(p,a):
    rows=read(p); row={'enrich_id':str(uuid.uuid4()),'time_utc':now(),'indicator':a.indicator,'indicator_type':a.indicator_type,'dns_note':a.dns_note,'whois_note':a.whois_note,'certificate_note':a.certificate_note,'hosting_note':a.hosting_note,'source_ref':a.source_ref,'confidence':a.confidence,'notes':a.notes}
    rows.append(row); save(p,rows); return row
def main():
    ap=argparse.ArgumentParser(description='Record DNS, WHOIS, certificate, and hosting enrichment notes for indicators.')
    ap.add_argument('log'); ap.add_argument('--indicator',required=True); ap.add_argument('--indicator-type',default='domain'); ap.add_argument('--dns-note',default=''); ap.add_argument('--whois-note',default=''); ap.add_argument('--certificate-note',default=''); ap.add_argument('--hosting-note',default=''); ap.add_argument('--source-ref',default=''); ap.add_argument('--confidence',default='low'); ap.add_argument('--notes',default=''); ap.add_argument('--list',action='store_true')
    a=ap.parse_args(); p=Path(a.log)
    if a.list: print(json.dumps(read(p),indent=2)); return 0
    print(json.dumps(add(p,a),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
