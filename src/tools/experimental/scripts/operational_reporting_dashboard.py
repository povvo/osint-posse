#!/usr/bin/env python3
"""Power BI / Tableau / Metabase operational reporting helper.

Prepares a clean metrics table and dashboard specification JSON for import into
BI tools or local reporting workflows.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(input_csv: Path, output_dir: Path, group_by: list[str]) -> dict:
    rows = read(input_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    specs = {"generated_utc": now(), "source": str(input_csv), "row_count": len(rows), "cards": [], "charts": []}
    specs["cards"].append({"title": "Total Rows", "value": len(rows)})
    for field in group_by:
        counts = dict(Counter(str(row.get(field, "blank") or "blank") for row in rows))
        specs["charts"].append({"field": field, "type": "bar", "counts": counts})
        with (output_dir / f"metric_{field}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=[field, "count"]); writer.writeheader()
            writer.writerows([{field: k, "count": v} for k, v in counts.items()])
    (output_dir / "dashboard_spec.json").write_text(json.dumps(specs, indent=2), encoding="utf-8")
    return {"output_dir": str(output_dir), "charts": len(specs["charts"]), "rows": len(rows)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare BI dashboard metric files from CSV.")
    ap.add_argument("input_csv"); ap.add_argument("--group-by", action="append", required=True); ap.add_argument("--output-dir", default="operational_dashboard")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.input_csv), Path(args.output_dir), args.group_by), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
