#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def build(layers_csv: Path, output_dir: Path):
    rows=read(layers_csv); output_dir.mkdir(parents=True, exist_ok=True)
    project={'layers':[],'notes':'Local GIS project manifest. Import layers into QGIS/ArcGIS manually.'}
    for r in rows:
        project['layers'].append({'name':r.get('name') or r.get('layer') or '', 'path':r.get('path') or r.get('locator') or '', 'type':r.get('type','unknown'), 'crs':r.get('crs',''), 'purpose':r.get('purpose','')})
    out=output_dir/'gis_project_manifest.json'; out.write_text(json.dumps(project, indent=2), encoding='utf-8')
    return {'output':str(out),'layers':len(project['layers'])}

def init(path: Path):
    fields=['name','path','type','crs','purpose']
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
    return {'created':str(path),'fields':fields}

def main():
    p=argparse.ArgumentParser(description='Create a GIS project manifest from layer records.')
    p.add_argument('--init'); p.add_argument('--layers'); p.add_argument('--output-dir', default='gis_project')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)), indent=2)); return 0
    if not a.layers: p.error('use --init or --layers')
    print(json.dumps(build(Path(a.layers), Path(a.output_dir)), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
