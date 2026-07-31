#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path


def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def compare(old_csv: Path, new_csv: Path, id_col: str):
    old={r.get(id_col):r for r in read(old_csv) if r.get(id_col)}; new={r.get(id_col):r for r in read(new_csv) if r.get(id_col)}
    added=[k for k in new if k not in old]; removed=[k for k in old if k not in new]
    changed=[]
    for k in old.keys() & new.keys():
        diffs={field:(old[k].get(field,''),new[k].get(field,'')) for field in set(old[k])|set(new[k]) if old[k].get(field,'')!=new[k].get(field,'')}
        if diffs: changed.append({'id':k,'changes':diffs})
    return {'old_records':len(old),'new_records':len(new),'added':added,'removed':removed,'changed':changed}

def main():
    p=argparse.ArgumentParser(description='Compare old/new map feature tables for urban morphology change.')
    p.add_argument('old_csv'); p.add_argument('new_csv'); p.add_argument('--id-col', default='id'); p.add_argument('--output', default='map_regression_report.json')
    a=p.parse_args(); result=compare(Path(a.old_csv), Path(a.new_csv), a.id_col); Path(a.output).write_text(json.dumps(result, indent=2), encoding='utf-8'); print(json.dumps({'output':a.output,'added':len(result['added']),'removed':len(result['removed']),'changed':len(result['changed'])}, indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
