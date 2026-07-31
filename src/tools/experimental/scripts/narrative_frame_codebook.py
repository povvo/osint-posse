#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from collections import Counter
from pathlib import Path
FIELDS=['frame','definition','actors','slogans','channels','example','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def apply(codebook:Path,textfile:Path,out:Path):
    with codebook.open(newline='',encoding='utf-8-sig') as f: frames=list(csv.DictReader(f))
    text=textfile.read_text(encoding='utf-8',errors='replace').lower(); hits=[]
    for fr in frames:
        terms=';'.join([fr.get('frame',''),fr.get('slogans',''),fr.get('actors','')]).split(';')
        count=sum(text.count(t.strip().lower()) for t in terms if t.strip())
        hits.append({'frame':fr.get('frame',''),'hits':count})
    out.write_text(json.dumps({'frames':hits},indent=2),encoding='utf-8'); return {'output':str(out),'frames':len(hits)}
def main():
    ap=argparse.ArgumentParser(description='Create or apply a narrative frame codebook to local text.')
    ap.add_argument('--init'); ap.add_argument('--codebook'); ap.add_argument('--text'); ap.add_argument('--output',default='frame_hits.json')
    a=ap.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.codebook or not a.text: ap.error('use --init or --codebook and --text')
    print(json.dumps(apply(Path(a.codebook),Path(a.text),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
