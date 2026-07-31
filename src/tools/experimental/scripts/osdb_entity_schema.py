#!/usr/bin/env python3
"""OSDb entity schema.

Defines and validates a compact entity schema for people, organisations, places,
events, assets, identifiers, and relationships. Exports JSON Schema and SQLite DDL.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ENTITY_TYPES = ["person", "organisation", "place", "event", "asset", "identifier", "document", "other"]
REL_TYPES = ["associated_with", "owns", "controls", "located_at", "mentions", "occurred_at", "part_of", "same_as"]
ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{3,120}$")


def entity_schema() -> dict:
    return {"type": "object", "required": ["id", "type", "label"], "properties": {"id": {"type": "string"}, "type": {"enum": ENTITY_TYPES}, "label": {"type": "string"}, "description": {"type": "string"}, "source_refs": {"type": "array", "items": {"type": "string"}}, "confidence": {"enum": ["low", "medium", "high"]}, "metadata": {"type": "object"}}}


def relation_schema() -> dict:
    return {"type": "object", "required": ["id", "source", "target", "type"], "properties": {"id": {"type": "string"}, "source": {"type": "string"}, "target": {"type": "string"}, "type": {"enum": REL_TYPES}, "source_refs": {"type": "array", "items": {"type": "string"}}, "confidence": {"enum": ["low", "medium", "high"]}, "metadata": {"type": "object"}}}


def validate_entity(row: dict) -> list[str]:
    errors = []
    if not ID_RE.match(str(row.get("id", ""))): errors.append("id is missing or unsafe")
    if row.get("type") not in ENTITY_TYPES: errors.append("unknown entity type")
    if not str(row.get("label", "")).strip(): errors.append("label is required")
    return errors


def validate_relation(row: dict, entity_ids: set[str]) -> list[str]:
    errors = []
    if not ID_RE.match(str(row.get("id", ""))): errors.append("id is missing or unsafe")
    if row.get("type") not in REL_TYPES: errors.append("unknown relationship type")
    if row.get("source") not in entity_ids: errors.append("source entity not present")
    if row.get("target") not in entity_ids: errors.append("target entity not present")
    return errors


def sqlite_ddl() -> str:
    return """CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  label TEXT NOT NULL,
  description TEXT,
  confidence TEXT DEFAULT 'low',
  metadata_json TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS relationships (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL REFERENCES entities(id),
  target TEXT NOT NULL REFERENCES entities(id),
  type TEXT NOT NULL,
  confidence TEXT DEFAULT 'low',
  metadata_json TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def validate_dataset(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    entities = data.get("entities", [])
    relations = data.get("relationships", [])
    ids = {e.get("id") for e in entities}
    findings = []
    for i, item in enumerate(entities, 1):
        for error in validate_entity(item): findings.append({"section": "entities", "row": i, "error": error})
    for i, item in enumerate(relations, 1):
        for error in validate_relation(item, ids): findings.append({"section": "relationships", "row": i, "error": error})
    return {"ok": not findings, "entity_count": len(entities), "relationship_count": len(relations), "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Export or validate an entity/relationship schema.")
    ap.add_argument("--json-schema")
    ap.add_argument("--sqlite-ddl")
    ap.add_argument("--validate")
    args = ap.parse_args()
    result = {"entity_schema": entity_schema(), "relationship_schema": relation_schema(), "entity_types": ENTITY_TYPES, "relationship_types": REL_TYPES}
    if args.json_schema: Path(args.json_schema).write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.sqlite_ddl: Path(args.sqlite_ddl).write_text(sqlite_ddl(), encoding="utf-8")
    if args.validate: result = validate_dataset(Path(args.validate))
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
