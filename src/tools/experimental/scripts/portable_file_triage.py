#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,re
from pathlib import Path
WORDS=re.compile(rb'[ -~]{4,}')
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def triage(path:Path,out:Path):
    data=path.read_bytes(); found=[m.group(0).decode('ascii','replace')[:200] for m in WORDS.finditer(data[:200000])][:200]
    result={'file':str(path),'bytes':len(data),'sha256':digest(path),'ascii_strings_preview':found,'notes':'local static preview only'}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),'strings_previewed':len(found)}
def main():
    ap=argparse.ArgumentParser(description='Create a local static triage preview for a portable file.')
    ap.add_argument('file'); ap.add_argument('--output',default='portable_file_triage.json')
    a=ap.parse_args(); print(json.dumps(triage(Path(a.file),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
