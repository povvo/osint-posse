#!/usr/bin/env python3
"""add_entity.

Adds or updates one entity in a local JSON entity store. The script preserves an
audit event for every change and rejects unsafe IDs or unsupported entity types.
"""
from __future__ import annotations
import argparse, json, re, uuid
from datetime import datetime, timezone
from pathlib import Path

ENTITY_TYPES = {"person", "organisation", "place", "event", "asset", "identifier", "document", "other"}
ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{3,120}$")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_store(path: Path) -> dict:
    if not path.exists():
        return {"entities": [], "audit": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("entities", []); data.setdefault("audit", [])
    return data


def save_store(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def make_id(label: str) -> str:
    base = re.sub(r"[^A-Za-z0-9_.:-]+", "_", label.strip()).strip("_")[:60]
    return f"ent:{base or 'entity'}:{uuid.uuid4().hex[:8]}"


def add_entity(path: Path, label: str, entity_type: str, source_ref: str, description: str = "", entity_id: str | None = None, confidence: str = "low") -> dict:
    if entity_type not in ENTITY_TYPES:
        raise ValueError(f"entity_type must be one of {sorted(ENTITY_TYPES)}")
    if confidence not in {"low", "medium", "high"}:
        raise ValueError("confidence must be low, medium, or high")
    if not label.strip():
        raise ValueError("label is required")
    entity_id = entity_id or make_id(label)
    if not ID_RE.match(entity_id):
        raise ValueError("entity id contains unsupported characters")
    data = load_store(path)
    existing = next((e for e in data["entities"] if e["id"] == entity_id), None)
    row = {"id": entity_id, "type": entity_type, "label": label, "description": description, "confidence": confidence, "source_refs": [source_ref] if source_ref else [], "updated_at_utc": now()}
    if existing:
        existing.update(row); action = "update"
    else:
        row["created_at_utc"] = now(); data["entities"].append(row); action = "create"
    data["audit"].append({"time_utc": now(), "action": action, "entity_id": entity_id, "source_ref": source_ref})
    save_store(path, data)
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description="Add or update an entity in a local JSON store.")
    ap.add_argument("store")
    ap.add_argument("--label", required=True)
    ap.add_argument("--type", required=True, choices=sorted(ENTITY_TYPES))
    ap.add_argument("--source-ref", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--id")
    ap.add_argument("--confidence", choices=["low", "medium", "high"], default="low")
    args = ap.parse_args()
    print(json.dumps(add_entity(Path(args.store), args.label, args.type, args.source_ref, args.description, args.id, args.confidence), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
