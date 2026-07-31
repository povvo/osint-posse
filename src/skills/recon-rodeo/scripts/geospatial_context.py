#!/usr/bin/env python3
"""
ospo :: geospatial context
Nearby OSM features, geocoding, reverse geocoding, haversine distance and bearing calculations.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict, field
from typing import Any

from osint_common import PublicSourceClient, ensure_dir, slugify, utc_now, write_json


@dataclass
class GeoFeature:
    source: str
    name: str
    feature_type: str
    lat: float | None = None
    lon: float | None = None
    tags: dict[str, Any] = field(default_factory=dict)
    distance_m: float | None = None
    bearing_deg: float | None = None


class NominatimClient:
    BASE = "https://nominatim.openstreetmap.org"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def geocode(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        data = self.http.get_json(f"{self.BASE}/search", params={"q": query, "format": "jsonv2", "limit": limit}, cache_ttl_seconds=86400)
        return data if isinstance(data, list) else []

    def reverse(self, lat: float, lon: float) -> dict[str, Any]:
        data = self.http.get_json(f"{self.BASE}/reverse", params={"lat": lat, "lon": lon, "format": "jsonv2"}, cache_ttl_seconds=86400)
        return data if isinstance(data, dict) else {"raw": data}


class OverpassClient:
    BASE = "https://overpass-api.de/api/interpreter"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def nearby(self, lat: float, lon: float, radius_m: int = 500, tags: list[str] | None = None) -> list[dict[str, Any]]:
        tags = tags or ["amenity", "shop", "tourism", "historic", "railway", "highway", "building"]
        filters = "\n".join(f'  nwr(around:{radius_m},{lat},{lon})["{tag}"];' for tag in tags)
        query = f"""
[out:json][timeout:25];
(
{filters}
);
out center tags 100;
"""
        response = self.http.get(self.BASE, params={"data": query}, cache_ttl_seconds=86400)
        try:
            data = json.loads(response.get("text", "{}"))
        except json.JSONDecodeError:
            data = {}
        return data.get("elements", [])


class GeospatialContext:
    def __init__(self, output_dir: str = "./geospatial_context"):
        self.output_dir = ensure_dir(output_dir)
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", min_interval_seconds=1.0)
        self.nominatim = NominatimClient(http)
        self.overpass = OverpassClient(http)

    def context_for_point(self, lat: float, lon: float, radius_m: int = 500) -> dict[str, Any]:
        reverse = self.nominatim.reverse(lat, lon)
        raw_features = self.overpass.nearby(lat, lon, radius_m)
        features: list[GeoFeature] = []
        for item in raw_features:
            tags = item.get("tags", {})
            flat = item.get("lat") or item.get("center", {}).get("lat")
            flon = item.get("lon") or item.get("center", {}).get("lon")
            feature = GeoFeature(
                source="openstreetmap_overpass",
                name=tags.get("name", ""),
                feature_type=item.get("type", ""),
                lat=flat,
                lon=flon,
                tags=tags,
            )
            if flat is not None and flon is not None:
                feature.distance_m = round(self.haversine_m(lat, lon, float(flat), float(flon)), 2)
                feature.bearing_deg = round(self.bearing(lat, lon, float(flat), float(flon)), 2)
            features.append(feature)
        features.sort(key=lambda f: f.distance_m if f.distance_m is not None else 10**9)
        result = {
            "point": {"lat": lat, "lon": lon, "radius_m": radius_m},
            "collected_at_utc": utc_now(),
            "reverse_geocode": reverse,
            "features": [asdict(f) for f in features],
            "total_features": len(features),
        }
        out = self.output_dir / f"geo_{lat}_{lon}.json"
        write_json(out, result)
        result["output_path"] = str(out)
        return result

    @staticmethod
    def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lam = math.radians(lon2 - lon1)
        a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
        return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    @staticmethod
    def bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        lam1, lam2 = math.radians(lon1), math.radians(lon2)
        y = math.sin(lam2 - lam1) * math.cos(phi2)
        x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(lam2 - lam1)
        return (math.degrees(math.atan2(y, x)) + 360) % 360


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect passive geospatial context around a coordinate")
    parser.add_argument("lat", type=float)
    parser.add_argument("lon", type=float)
    parser.add_argument("--radius", type=int, default=500)
    parser.add_argument("--out-dir", default="./geospatial_context")
    args = parser.parse_args()
    print(json.dumps(GeospatialContext(args.out_dir).context_for_point(args.lat, args.lon, args.radius), indent=2))


if __name__ == "__main__":
    main()
