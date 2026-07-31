#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
FIELDS=['asset_id','name','category','lat','lon','address','owner','service','risk','notes']
def read(p):
    if not p.exists(): return []
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def geojson(csv_path:Path,out:Path):
    feats=[]; bad=[]
    for i,r in enumerate(read(csv_path),1):
        try:
            lat=float(r.get('lat','')); lon=float(r.get('lon',''))
            feats.append({'type':'Feature','geometry':{'type':'Point','coordinates':[lon,lat]},'properties':{k:v for k,v in r.items() if k not in {'lat','lon'}}})
        except Exception as e: bad.append({'row':i,'error':str(e)})
    out.write_text(json.dumps({'type':'FeatureCollection','features':feats},indent=2),encoding='utf-8')
    return {'output':str(out),'features':len(feats),'rejected':bad}
def main():
    p=argparse.ArgumentParser(description='Create or export a community asset map CSV to GeoJSON.')
    p.add_argument('--init'); p.add_argument('--geojson'); p.add_argument('--output',default='community_assets.geojson')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.geojson: p.error('use --init or --geojson')
    print(json.dumps(geojson(Path(a.geojson),Path(a.output)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
