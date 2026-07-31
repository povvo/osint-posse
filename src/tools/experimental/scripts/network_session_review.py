#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from collections import Counter
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def analyse(p:Path,out:Path):
    rows=read(p); proto=Counter(r.get('protocol','unknown') for r in rows); pairs=Counter((r.get('source',''),r.get('destination','')) for r in rows)
    result={'rows':len(rows),'protocols':dict(proto),'top_pairs':[{'source':a,'destination':b,'count':c} for (a,b),c in pairs.most_common(20)]}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),'rows':len(rows),'protocols':len(proto)}
def main():
    ap=argparse.ArgumentParser(description='Summarise network session CSV rows by protocol and endpoint pair.')
    ap.add_argument('sessions_csv'); ap.add_argument('--output',default='network_session_summary.json')
    a=ap.parse_args(); print(json.dumps(analyse(Path(a.sessions_csv),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
