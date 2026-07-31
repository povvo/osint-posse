#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
SECTIONS=['Participant','Project','Material','Permitted uses','Restrictions','Withdrawal terms','Contact','Signature']
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def create(name,project,out:Path):
    lines=[f'# Consent and Release Form', '', f'Participant: {name}', f'Project: {project}', f'Created: {now()}', '']
    for s in SECTIONS: lines += [f'## {s}', '', '- ', '']
    out.write_text('\n'.join(lines),encoding='utf-8')
    return {'output':str(out),'sections':SECTIONS}
def main():
    p=argparse.ArgumentParser(description='Create a consent and release form template for oral-history material.')
    p.add_argument('--name',default=''); p.add_argument('--project',default=''); p.add_argument('--output',default='release_form.md')
    a=p.parse_args(); print(json.dumps(create(a.name,a.project,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
