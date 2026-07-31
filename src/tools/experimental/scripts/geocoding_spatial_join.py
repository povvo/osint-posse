#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path

def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def dist(a,b): return math.hypot(float(a.get('lat',0))-float(b.get('lat',0)), float(a.get('lon',0))-float(b.get('lon',0)))
def join(points:Path,areas:Path,out:Path,threshold:float):
    pts,ars=read(points),read(areas); rows=[]
    for p in pts:
        candidates=[]
        for a in ars:
            try: candidates.append((dist(p,a),a))
            except Exception: pass
        candidates.sort(key=lambda x:x[0])
        best=candidates[0] if candidates else None
        row=dict(p)
        if best and best[0]<=threshold:
            row['joined_area']=best[1].get('area_id') or best[1].get('name') or ''
            row['join_distance']=round(best[0],6)
        else:
            row['joined_area']=''; row['join_distance']=''
        rows.append(row)
    fields=sorted({k for r in rows for k in r}) if rows else []
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    return {'output':str(out),'points':len(pts),'areas':len(ars),'joined':sum(1 for r in rows if r.get('joined_area'))}
def main():
    ap=argparse.ArgumentParser(description='Join coordinate CSV points to nearest area/feature rows by distance threshold.')
    ap.add_argument('points_csv'); ap.add_argument('areas_csv'); ap.add_argument('--threshold',type=float,default=0.1); ap.add_argument('--output',default='spatial_join.csv')
    a=ap.parse_args(); print(json.dumps(join(Path(a.points_csv),Path(a.areas_csv),Path(a.output),a.threshold),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
