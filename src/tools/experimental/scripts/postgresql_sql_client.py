#!/usr/bin/env python3
"""PostgreSQL / SQL client helper.

Generates safe SQL files from CSV schemas and optionally runs read-only SQLite
checks for local validation. It does not open network database connections.
"""
from __future__ import annotations
import argparse, csv, json, re, sqlite3
from pathlib import Path

SAFE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,62}$")


def ident(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip().lower()).strip("_")
    if not cleaned or cleaned[0].isdigit(): cleaned = "c_" + cleaned
    return cleaned[:63]


def infer_type(values: list[str]) -> str:
    vals = [v for v in values if v not in (None, "")]
    if vals and all(str(v).isdigit() for v in vals): return "INTEGER"
    for val in vals:
        try: float(val)
        except Exception: return "TEXT"
    return "REAL" if vals else "TEXT"


def create_table_sql(csv_path: Path, table: str) -> dict:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    fields = list(rows[0].keys()) if rows else []
    columns = []
    for field in fields:
        name = ident(field)
        typ = infer_type([row.get(field, "") for row in rows])
        columns.append({"source": field, "name": name, "type": typ})
    sql = "CREATE TABLE IF NOT EXISTS " + ident(table) + " (\n  " + ",\n  ".join(f"{c['name']} {c['type']}" for c in columns) + "\n);\n"
    return {"table": ident(table), "columns": columns, "sql": sql, "rows_profiled": len(rows)}


def sqlite_check(csv_path: Path, table: str) -> dict:
    spec = create_table_sql(csv_path, table)
    con = sqlite3.connect(":memory:")
    con.execute(spec["sql"])
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    names = [c["name"] for c in spec["columns"]]
    placeholders = ",".join("?" for _ in names)
    for row in rows:
        values = [row.get(c["source"], "") for c in spec["columns"]]
        con.execute(f"INSERT INTO {spec['table']} ({','.join(names)}) VALUES ({placeholders})", values)
    count = con.execute(f"SELECT COUNT(*) FROM {spec['table']}").fetchone()[0]
    return {"table": spec["table"], "inserted_rows": count, "column_count": len(names)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate SQL schema from CSV and run local validation.")
    ap.add_argument("csv")
    ap.add_argument("--table", required=True)
    ap.add_argument("--write-sql")
    ap.add_argument("--sqlite-check", action="store_true")
    args = ap.parse_args()
    result = create_table_sql(Path(args.csv), args.table)
    if args.write_sql: Path(args.write_sql).write_text(result["sql"], encoding="utf-8")
    if args.sqlite_check: result["sqlite_check"] = sqlite_check(Path(args.csv), args.table)
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
