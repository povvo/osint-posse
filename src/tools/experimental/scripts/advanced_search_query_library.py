#!/usr/bin/env python3
"""Advanced search query library.

Stores reusable search-query templates with placeholders, renders concrete query
sets, and records intended source type and review notes.
"""
from __future__ import annotations
import argparse, json, re, uuid
from datetime import datetime, timezone
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> list[dict]:
    if not path.exists(): return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def add_template(path: Path, name: str, query: str, source_type: str, notes: str) -> dict:
    rows = load(path)
    item = {"id": str(uuid.uuid4()), "name": name, "query": query, "source_type": source_type, "placeholders": sorted(set(PLACEHOLDER.findall(query))), "notes": notes, "created_utc": now()}
    rows.append(item); save(path, rows); return item


def parse_params(items: list[str]) -> dict[str, str]:
    params = {}
    for item in items:
        if "=" not in item: raise ValueError(f"expected key=value: {item}")
        key, value = item.split("=", 1); params[key] = value
    return params


def render(path: Path, name_or_id: str, params: dict[str, str]) -> dict:
    item = next((r for r in load(path) if r["id"].startswith(name_or_id) or r["name"] == name_or_id), None)
    if not item: raise KeyError("template not found")
    missing = [p for p in item["placeholders"] if p not in params]
    if missing: raise ValueError(f"missing placeholders: {missing}")
    query = item["query"]
    for key, value in params.items():
        query = query.replace("{{" + key + "}}", value)
    return {"template": item["name"], "source_type": item["source_type"], "query": query, "rendered_utc": now()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Maintain and render reusable search-query templates.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add"); add.add_argument("library"); add.add_argument("--name", required=True); add.add_argument("--query", required=True); add.add_argument("--source-type", default="web"); add.add_argument("--notes", default="")
    ren = sub.add_parser("render"); ren.add_argument("library"); ren.add_argument("name_or_id"); ren.add_argument("--param", action="append", default=[])
    ls = sub.add_parser("list"); ls.add_argument("library")
    args = parser.parse_args()
    if args.cmd == "add": print(json.dumps(add_template(Path(args.library), args.name, args.query, args.source_type, args.notes), indent=2)); return 0
    if args.cmd == "render": print(json.dumps(render(Path(args.library), args.name_or_id, parse_params(args.param)), indent=2)); return 0
    print(json.dumps(load(Path(args.library)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
