#!/usr/bin/env python3
"""Spreadsheet / CSV workspace.

Profiles CSV files, normalises column names, deduplicates rows, and exports a
clean workspace package with a data dictionary and quality report.
"""
from __future__ import annotations
import argparse, csv, json, re
from collections import Counter
from pathlib import Path


def clean_header(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().lower()).strip("_")
    return name or "column"


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def normalise_rows(headers: list[str], rows: list[dict]) -> tuple[list[str], list[dict]]:
    seen: Counter[str] = Counter()
    mapping: dict[str, str] = {}
    for header in headers:
        base = clean_header(header)
        seen[base] += 1
        mapping[header] = base if seen[base] == 1 else f"{base}_{seen[base]}"
    clean_rows = []
    for row in rows:
        clean_rows.append({mapping[k]: v for k, v in row.items() if k in mapping})
    return list(mapping.values()), clean_rows


def profile(headers: list[str], rows: list[dict]) -> dict:
    columns = []
    for header in headers:
        values = [row.get(header, "") for row in rows]
        non_empty = [v for v in values if v not in (None, "")]
        columns.append({"column": header, "rows": len(values), "non_empty": len(non_empty), "blank": len(values) - len(non_empty), "unique": len(set(non_empty)), "sample": non_empty[:5]})
    fingerprints = [tuple(row.get(h, "") for h in headers) for row in rows]
    return {"row_count": len(rows), "column_count": len(headers), "duplicate_rows": len(fingerprints) - len(set(fingerprints)), "columns": columns}


def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def build_workspace(input_csv: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    original_headers, rows = read_csv(input_csv)
    headers, clean_rows = normalise_rows(original_headers, rows)
    unique_rows = list({tuple(row.get(h, "") for h in headers): row for row in clean_rows}.values())
    clean_path = output_dir / "clean.csv"
    write_csv(clean_path, headers, unique_rows)
    report = {"input": str(input_csv), "clean_csv": str(clean_path), "original": profile(original_headers, rows), "clean": profile(headers, unique_rows), "header_mapping": dict(zip(original_headers, headers))}
    (output_dir / "quality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a clean CSV workspace and quality report.")
    ap.add_argument("input_csv")
    ap.add_argument("--output-dir", default="csv_workspace")
    args = ap.parse_args()
    print(json.dumps(build_workspace(Path(args.input_csv), Path(args.output_dir)), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
