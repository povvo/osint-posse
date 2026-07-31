#!/usr/bin/env python3
"""Protégé / ontology editor helper.

Creates an ontology editing package: class/property CSVs, Turtle starter file, and
an issues report for duplicate class/property names.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path


def safe_term(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip()).strip("_")
    if not text or not text[0].isalpha(): text = "Term_" + text
    return text


def init_package(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    class_rows = [{"class": "Entity", "parent": "Thing", "definition": "Root investigative object"}, {"class": "Person", "parent": "Entity", "definition": "Human actor"}]
    prop_rows = [{"property": "relatedTo", "domain": "Entity", "range": "Entity", "definition": "Generic relationship pending refinement"}]
    for name, rows, fields in [("classes.csv", class_rows, ["class", "parent", "definition"]), ("properties.csv", prop_rows, ["property", "domain", "range", "definition"])]:
        with (output_dir / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    ttl = "@prefix : <https://example.invalid/ontology/> .\n:Entity a :Class .\n:Person a :Class ; :subClassOf :Entity .\n:relatedTo a :ObjectProperty .\n"
    (output_dir / "ontology_starter.ttl").write_text(ttl, encoding="utf-8")
    return {"output_dir": str(output_dir), "files": ["classes.csv", "properties.csv", "ontology_starter.ttl"]}


def validate(classes: Path, properties: Path) -> dict:
    findings = []
    def read(path: Path) -> list[dict]:
        with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))
    class_rows, prop_rows = read(classes), read(properties)
    names = [safe_term(r.get("class", "")) for r in class_rows]
    props = [safe_term(r.get("property", "")) for r in prop_rows]
    for value in sorted({x for x in names if names.count(x) > 1}): findings.append({"type": "duplicate_class", "value": value})
    for value in sorted({x for x in props if props.count(x) > 1}): findings.append({"type": "duplicate_property", "value": value})
    return {"classes": len(class_rows), "properties": len(prop_rows), "ok": not findings, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or validate an ontology editing package.")
    ap.add_argument("--init")
    ap.add_argument("--classes"); ap.add_argument("--properties")
    args = ap.parse_args()
    if args.init: print(json.dumps(init_package(Path(args.init)), indent=2)); return 0
    if not args.classes or not args.properties: ap.error("use --init or provide --classes and --properties")
    print(json.dumps(validate(Path(args.classes), Path(args.properties)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
