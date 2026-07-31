#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from collections import Counter
from pathlib import Path

def read_texts(paths):
    rows=[]
    for p in paths:
        text=Path(p).read_text(encoding='utf-8',errors='replace')
        rows.append({'path':str(p),'text':text})
    return rows
def analyse(paths,out:Path):
    docs=read_texts(paths); words=Counter(); sentiment=0
    pos={'good','gain','support','safe','positive'}; neg={'bad','loss','risk','harm','negative'}
    for d in docs:
        tokens=re.findall(r'[A-Za-z]{4,}',d['text'].lower()); words.update(tokens); sentiment+=sum(1 for t in tokens if t in pos)-sum(1 for t in tokens if t in neg)
    result={'documents':len(docs),'top_terms':words.most_common(50),'sentiment_balance':sentiment}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8'); return {'output':str(out),**result}
def main():
    ap=argparse.ArgumentParser(description='Run simple local topic and sentiment counts over text files.')
    ap.add_argument('texts',nargs='+'); ap.add_argument('--output',default='nlp_topic_summary.json')
    a=ap.parse_args(); print(json.dumps(analyse(a.texts,Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
