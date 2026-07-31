#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def layer(p:Path,out:Path,name:str):
    rows=read(p); techniques=[]
    for r in rows:
        tid=r.get('technique_id') or r.get('id') or ''
        if tid: techniques.append({'techniqueID':tid,'score':float(r.get('score',1) or 1),'comment':r.get('comment','')})
    data={'name':name,'version':'4.5','domain':'enterprise-attack','techniques':techniques}
    out.write_text(json.dumps(data,indent=2),encoding='utf-8'); return {'output':str(out),'techniques':len(techniques)}
def main():
    ap=argparse.ArgumentParser(description='Create a MITRE ATT&CK Navigator layer JSON from technique rows.')
    ap.add_argument('techniques_csv'); ap.add_argument('--name',default='Coverage layer'); ap.add_argument('--output',default='attack_navigator_layer.json')
    a=ap.parse_args(); print(json.dumps(layer(Path(a.techniques_csv),Path(a.output),a.name),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
