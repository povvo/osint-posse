#!/usr/bin/env python3
"""
ospo :: visualisation suite
Simple charts, maps and HTML index pages for investigation outputs.
"""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

from osint_common import ensure_dir, read_json, utc_now, write_json

try:
    import matplotlib.pyplot as plt  # type: ignore
    HAS_MATPLOTLIB = True
except Exception:
    HAS_MATPLOTLIB = False

try:
    import folium  # type: ignore
    HAS_FOLIUM = True
except Exception:
    HAS_FOLIUM = False


class VisualisationSuite:
    def __init__(self, output_dir: str = "./visualisations"):
        self.output_dir = ensure_dir(output_dir)

    def bar_chart(self, counts: dict[str, int], title: str, filename: str = "bar_chart.png") -> dict[str, Any]:
        if not HAS_MATPLOTLIB:
            return {"error": "matplotlib not installed"}
        labels = list(counts.keys())[:30]
        values = [counts[k] for k in labels]
        plt.figure(figsize=(max(8, len(labels) * 0.45), 5))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.title(title)
        plt.tight_layout()
        out = self.output_dir / filename
        plt.savefig(out, dpi=160)
        plt.close()
        return {"path": str(out), "count": len(labels)}

    def timeline_chart(self, events: list[dict[str, Any]], filename: str = "timeline_counts.png") -> dict[str, Any]:
        counts = Counter((e.get("utc_datetime") or e.get("date") or "")[:10] for e in events)
        counts.pop("", None)
        return self.bar_chart(dict(sorted(counts.items())), "Events by day", filename)

    def map_points(self, points: list[dict[str, Any]], filename: str = "points_map.html") -> dict[str, Any]:
        if not HAS_FOLIUM:
            return {"error": "folium not installed"}
        valid = [p for p in points if p.get("lat") is not None and p.get("lon") is not None]
        if not valid:
            return {"error": "no points with lat/lon"}
        centre = [sum(float(p["lat"]) for p in valid) / len(valid), sum(float(p["lon"]) for p in valid) / len(valid)]
        m = folium.Map(location=centre, zoom_start=12)  # type: ignore[name-defined]
        for p in valid:
            folium.Marker([float(p["lat"]), float(p["lon"])], popup=html.escape(str(p.get("label", "point")))).add_to(m)  # type: ignore[name-defined]
        out = self.output_dir / filename
        m.save(str(out))
        return {"path": str(out), "points": len(valid)}

    def html_index(self, artefacts: list[str], title: str = "OSINT Artefact Index", filename: str = "index.html") -> str:
        rows = []
        for artefact in artefacts:
            p = Path(artefact)
            rel = html.escape(p.name)
            rows.append(f"<li><a href='{html.escape(str(p))}'>{rel}</a></li>")
        page = f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><title>{html.escape(title)}</title>
<style>body{{font-family:Arial,sans-serif;max-width:960px;margin:40px auto;line-height:1.5}}code{{background:#eee;padding:2px 4px}}</style></head>
<body><h1>{html.escape(title)}</h1><p>Generated {utc_now()}</p><ul>{''.join(rows)}</ul></body></html>"""
        out = self.output_dir / filename
        out.write_text(page, encoding="utf-8")
        return str(out)

    def visualise_json(self, path: str) -> dict[str, Any]:
        data = read_json(path)
        artefacts: list[str] = []
        if isinstance(data, dict) and "articles" in data:
            counts = Counter(a.get("domain", "unknown") for a in data["articles"] if isinstance(a, dict))
            artefacts.append(self.bar_chart(dict(counts.most_common(20)), "Article domains", "article_domains.png").get("path", ""))
        if isinstance(data, dict) and "events" in data:
            artefacts.append(self.timeline_chart(data["events"]).get("path", ""))
        if isinstance(data, dict) and "features" in data:
            points = [{"lat": f.get("lat"), "lon": f.get("lon"), "label": f.get("name") or f.get("feature_type")} for f in data["features"]]
            artefacts.append(self.map_points(points, "features_map.html").get("path", ""))
        artefacts = [a for a in artefacts if a]
        index = self.html_index(artefacts)
        return {"input": path, "artefacts": artefacts, "index": index}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create simple visualisations from OSINT JSON outputs")
    parser.add_argument("json_path")
    parser.add_argument("--out-dir", default="./visualisations")
    args = parser.parse_args()
    print(json.dumps(VisualisationSuite(args.out_dir).visualise_json(args.json_path), indent=2))


if __name__ == "__main__":
    main()
