#!/usr/bin/env python3
"""geolocation.py.

Local coordinate utility: validates latitude/longitude, calculates distance, and
exports point CSV rows as GeoJSON. No network calls are made.
"""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path


def check(lat: float, lon: float) -> None:
    if lat < -90 or lat > 90:
        raise ValueError("latitude out of range")
    if lon < -180 or lon > 180:
        raise ValueError("longitude out of range")


def haversine(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    check(a_lat, a_lon); check(b_lat, b_lon)
    radius = 6371.0088
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dphi = math.radians(b_lat - a_lat)
    dlambda = math.radians(b_lon - a_lon)
    value = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return radius * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def to_geojson(input_csv: Path, output: Path, lat_col: str, lon_col: str) -> dict:
    features = []
    rejected = []
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), 1):
            try:
                lat = float(row[lat_col]); lon = float(row[lon_col]); check(lat, lon)
                features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]}, "properties": {k: v for k, v in row.items() if k not in {lat_col, lon_col}}})
            except Exception as exc:
                rejected.append({"row": row_number, "error": str(exc)})
    output.write_text(json.dumps({"type": "FeatureCollection", "features": features}, indent=2), encoding="utf-8")
    return {"output": str(output), "features": len(features), "rejected": rejected}


def main() -> int:
    parser = argparse.ArgumentParser(description="Local coordinate checks and GeoJSON export.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    dist = sub.add_parser("distance")
    dist.add_argument("a_lat", type=float); dist.add_argument("a_lon", type=float); dist.add_argument("b_lat", type=float); dist.add_argument("b_lon", type=float)
    geo = sub.add_parser("geojson")
    geo.add_argument("input_csv"); geo.add_argument("--lat-col", default="lat"); geo.add_argument("--lon-col", default="lon"); geo.add_argument("--output", default="points.geojson")
    args = parser.parse_args()
    if args.cmd == "distance":
        print(json.dumps({"distance_km": round(haversine(args.a_lat, args.a_lon, args.b_lat, args.b_lon), 6)}, indent=2)); return 0
    print(json.dumps(to_geojson(Path(args.input_csv), Path(args.output), args.lat_col, args.lon_col), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
