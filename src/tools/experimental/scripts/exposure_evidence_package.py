#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from datetime import datetime,timezone
from pathlib import Path
SECTIONS=['Subject','Basis','Source-backed indicators','Screening results','Ownership/control links','Caveats','Reviewer decision']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def create(subject,out:Path):
    lines=[f'# Exposure Evidence Package: {subject}','',f'Created: {now()}','']
    for s in SECTIONS: lines += [f'## {s}','','- ','']
    out.write_text('\n'.join(lines),encoding='utf-8'); return {'output':str(out),'sections':SECTIONS}
def main():
    ap=argparse.ArgumentParser(description='Create a source-backed exposure evidence package template.')
    ap.add_argument('--subject',required=True); ap.add_argument('--output',default='exposure_evidence_package.md')
    a=ap.parse_args(); print(json.dumps(create(a.subject,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
