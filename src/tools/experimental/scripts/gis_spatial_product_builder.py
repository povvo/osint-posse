#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def geojson(p:Path,out:Path,lat_col:str,lon_col:str):
    feats=[]; bad=[]
    for i,r in enumerate(read(p),1):
        try:
            lat=float(r[lat_col]); lon=float(r[lon_col]);
            if not (-90<=lat<=90 and -180<=lon<=180): raise ValueError('coordinate out of range')
            feats.append({'type':'Feature','geometry':{'type':'Point','coordinates':[lon,lat]},'properties':{k:v for k,v in r.items() if k not in {lat_col,lon_col}}})
        except Exception as e: bad.append({'row':i,'error':str(e)})
    out.write_text(json.dumps({'type':'FeatureCollection','features':feats},indent=2),encoding='utf-8'); return {'output':str(out),'features':len(feats),'rejected':bad}
def main():
    ap=argparse.ArgumentParser(description='Create a GeoJSON spatial product from coordinate CSV rows.')
    ap.add_argument('csv'); ap.add_argument('--lat-col',default='lat'); ap.add_argument('--lon-col',default='lon'); ap.add_argument('--output',default='spatial_product.geojson')
    a=ap.parse_args(); print(json.dumps(geojson(Path(a.csv),Path(a.output),a.lat_col,a.lon_col),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
