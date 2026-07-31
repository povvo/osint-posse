#!/usr/bin/env python3
"""ETL / ELT local table pipeline.

Reads CSV or JSON records, renames fields, removes rows with blank required
values, and writes a clean CSV plus a load manifest.
"""
from __future__ import annotations
import argparse, csv, json, re
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_col(name: str) -> str:
    col = re.sub(r"[^A-Za-z0-9]+", "_", name.strip().lower()).strip("_")
    return col or "column"


def read_records(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def parse_renames(items: list[str]) -> dict[str, str]:
    mapping = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"rename must be old=new: {item}")
        old, new = item.split("=", 1)
        mapping[old] = new
    return mapping


def transform(rows: list[dict], renames: dict[str, str], required_key: str | None) -> list[dict]:
    output = []
    for row in rows:
        if required_key and not str(row.get(required_key, "")).strip():
            continue
        clean = {safe_col(renames.get(key, key)): value for key, value in row.items()}
        clean["loaded_at_utc"] = now()
        output.append(clean)
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = sorted({key for row in rows for key in row})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def run(input_path: Path, output_csv: Path, rename: list[str], required_key: str | None) -> dict:
    rows = read_records(input_path)
    transformed = transform(rows, parse_renames(rename), required_key)
    write_csv(output_csv, transformed)
    manifest = {"input": str(input_path), "output": str(output_csv), "input_rows": len(rows), "output_rows": len(transformed), "columns": sorted({k for r in transformed for k in r})}
    output_csv.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a local CSV/JSON table transform.")
    ap.add_argument("input")
    ap.add_argument("--output", default="clean_table.csv")
    ap.add_argument("--rename", action="append", default=[])
    ap.add_argument("--required-key")
    args = ap.parse_args()
    print(json.dumps(run(Path(args.input), Path(args.output), args.rename, args.required_key), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
