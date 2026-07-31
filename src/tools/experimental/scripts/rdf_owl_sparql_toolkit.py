#!/usr/bin/env python3
"""RDF/OWL triplestore and SPARQL helper.

Builds simple Turtle triples from CSV rows and creates SPARQL SELECT templates
for entity and relationship review.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

BASE = "https://example.invalid/resource/"


def iri(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value).strip()).strip("_")
    return f"<{BASE}{cleaned or 'item'}>"


def lit(value: str) -> str:
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"') + '"'


def pred(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", str(value).strip()).strip("_")
    return f":{cleaned or 'value'}"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def csv_to_turtle(input_csv: Path, id_col: str, class_name: str, output: Path) -> dict:
    rows = read_csv(input_csv)
    lines = ["@prefix : <https://example.invalid/vocab/> .", f"@prefix r: <{BASE}> .", ""]
    findings = []
    for idx, row in enumerate(rows, 1):
        rid = row.get(id_col)
        if not rid:
            findings.append({"row": idx, "issue": f"missing {id_col}"}); continue
        subject = iri(rid)
        lines.append(f"{subject} a :{class_name} .")
        for key, value in row.items():
            if key == id_col or value in (None, ""): continue
            lines.append(f"{subject} {pred(key)} {lit(value)} .")
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"input": str(input_csv), "output": str(output), "rows": len(rows), "findings": findings, "ok": not findings}


def sparql_templates(output: Path) -> dict:
    text = """PREFIX : <https://example.invalid/vocab/>

# List instances by class
SELECT ?item ?label WHERE {
  ?item a :Entity .
  OPTIONAL { ?item :label ?label }
}

# Find relationships mentioning a value
SELECT ?s ?p ?o WHERE {
  ?s ?p ?o .
  FILTER(CONTAINS(LCASE(STR(?o)), "search term"))
}
"""
    output.write_text(text, encoding="utf-8")
    return {"output": str(output)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create Turtle triples or SPARQL templates.")
    ap.add_argument("--csv")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--class-name", default="Entity")
    ap.add_argument("--turtle-output", default="entities.ttl")
    ap.add_argument("--sparql-output")
    args = ap.parse_args()
    result = {}
    if args.csv: result["turtle"] = csv_to_turtle(Path(args.csv), args.id_col, args.class_name, Path(args.turtle_output))
    if args.sparql_output: result["sparql"] = sparql_templates(Path(args.sparql_output))
    if not result: ap.error("use --csv and/or --sparql-output")
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
