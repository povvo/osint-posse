#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def sigma(title:str,logsource:str,field:str,value:str):
    return f"title: {title}\nstatus: experimental\nlogsource:\n  product: {logsource}\ndetection:\n  selection:\n    {field}: '{value}'\n  condition: selection\nfields:\n  - {field}\nfalsepositives:\n  - Unknown\nlevel: medium\n"
def yara(name:str,string_id:str,value:str):
    safe=re.sub(r'[^A-Za-z0-9_]+','_',name)
    return f"rule {safe} {{\n  strings:\n    ${string_id} = \"{value}\"\n  condition:\n    ${string_id}\n}}\n"
def main():
    ap=argparse.ArgumentParser(description='Create simple local YARA or Sigma detection rule templates.')
    ap.add_argument('--kind',choices=['yara','sigma'],required=True); ap.add_argument('--name',required=True); ap.add_argument('--field',default='message'); ap.add_argument('--value',required=True); ap.add_argument('--output',required=True); ap.add_argument('--logsource',default='windows')
    a=ap.parse_args(); text=yara(a.name,'s1',a.value) if a.kind=='yara' else sigma(a.name,a.logsource,a.field,a.value); Path(a.output).write_text(text,encoding='utf-8'); print(json.dumps({'output':a.output,'kind':a.kind},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
