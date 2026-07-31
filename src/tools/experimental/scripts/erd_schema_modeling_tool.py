#!/usr/bin/env python3
"""ERD/schema modelling tool.

Reads table definitions from CSV and writes Mermaid ER diagrams plus a foreign key
review report.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def read_defs(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def safe(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip()).strip("_")
    if not name or name[0].isdigit(): name = "T_" + name
    return name


def build(rows: list[dict]) -> tuple[str, dict]:
    tables: dict[str, list[dict]] = {}
    relationships = []
    findings = []
    for idx, row in enumerate(rows, 1):
        table = safe(row.get("table", "")); column = safe(row.get("column", ""))
        if not table or not column:
            findings.append({"row": idx, "issue": "table and column required"}); continue
        tables.setdefault(table, []).append(row)
        ref_table = row.get("references_table", "").strip()
        ref_column = row.get("references_column", "").strip()
        if ref_table and ref_column:
            relationships.append((table, safe(ref_table), row.get("relationship", "references") or "references"))
    lines = ["erDiagram"]
    for table, cols in sorted(tables.items()):
        lines.append(f"  {table} {{")
        for col in cols:
            typ = safe(col.get("type", "TEXT") or "TEXT")
            key = "PK" if str(col.get("primary_key", "")).lower() in {"1", "true", "yes"} else ""
            lines.append(f"    {typ} {safe(col.get('column',''))} {key}".rstrip())
        lines.append("  }")
    for left, right, label in relationships:
        lines.append(f"  {right} ||--o{{ {left} : {safe(label)}")
    return "\n".join(lines) + "\n", {"tables": len(tables), "relationships": len(relationships), "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create Mermaid ERD from table definition CSV.")
    ap.add_argument("definition_csv")
    ap.add_argument("--output", default="schema_erd.mmd")
    args = ap.parse_args()
    mermaid, report = build(read_defs(Path(args.definition_csv)))
    Path(args.output).write_text(mermaid, encoding="utf-8")
    report["output"] = args.output
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
