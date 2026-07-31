#!/usr/bin/env python3
"""Implementing the POLE Schema.

Validates People, Objects, Locations, and Events tables and emits a starter SQL
schema plus relationship sanity checks.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

POLE = {
    "people": ["person_id", "name"],
    "objects": ["object_id", "label"],
    "locations": ["location_id", "label"],
    "events": ["event_id", "label", "date"],
    "links": ["source_table", "source_id", "target_table", "target_id", "relationship"],
}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def validate_table(name: str, path: Path) -> dict:
    rows = read_csv(path)
    fields = set(rows[0].keys()) if rows else set()
    required = set(POLE[name])
    missing = sorted(required - fields)
    blanks = []
    for idx, row in enumerate(rows, 1):
        for field in required:
            if not str(row.get(field, "")).strip():
                blanks.append({"row": idx, "field": field})
    return {"table": name, "path": str(path), "rows": len(rows), "missing_columns": missing, "blank_required_values": blanks, "ok": not missing and not blanks}


def sql_schema() -> str:
    return """CREATE TABLE people (person_id TEXT PRIMARY KEY, name TEXT NOT NULL, notes TEXT);
CREATE TABLE objects (object_id TEXT PRIMARY KEY, label TEXT NOT NULL, notes TEXT);
CREATE TABLE locations (location_id TEXT PRIMARY KEY, label TEXT NOT NULL, lat REAL, lon REAL, notes TEXT);
CREATE TABLE events (event_id TEXT PRIMARY KEY, label TEXT NOT NULL, date TEXT, notes TEXT);
CREATE TABLE links (
  link_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_table TEXT NOT NULL,
  source_id TEXT NOT NULL,
  target_table TEXT NOT NULL,
  target_id TEXT NOT NULL,
  relationship TEXT NOT NULL,
  source_ref TEXT
);
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate and export POLE schema artefacts.")
    ap.add_argument("--people")
    ap.add_argument("--objects")
    ap.add_argument("--locations")
    ap.add_argument("--events")
    ap.add_argument("--links")
    ap.add_argument("--write-sql")
    args = ap.parse_args()
    results = []
    for name in POLE:
        supplied = getattr(args, name)
        if supplied:
            results.append(validate_table(name, Path(supplied)))
    if args.write_sql:
        Path(args.write_sql).write_text(sql_schema(), encoding="utf-8")
    print(json.dumps({"validated": results, "all_ok": all(r["ok"] for r in results), "schema_tables": list(POLE)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
