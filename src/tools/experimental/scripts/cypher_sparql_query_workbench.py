#!/usr/bin/env python3
"""Cypher/SPARQL query workbench.

Maintains a local library of graph query templates, validates parameter markers,
and renders parameterised query files without connecting to a database.
"""
from __future__ import annotations
import argparse, json, re, uuid
from datetime import datetime, timezone
from pathlib import Path

PARAM_RE = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> list[dict]:
    if not path.exists(): return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def add_template(path: Path, name: str, language: str, query_file: Path, notes: str) -> dict:
    if language not in {"cypher", "sparql"}: raise ValueError("language must be cypher or sparql")
    query = query_file.read_text(encoding="utf-8")
    item = {"id": str(uuid.uuid4()), "name": name, "language": language, "query": query, "parameters": sorted(set(PARAM_RE.findall(query))), "notes": notes, "created_at_utc": now()}
    rows = load(path); rows.append(item); save(path, rows); return item


def render(path: Path, template_id: str, params: dict[str, str], output: Path) -> dict:
    item = next((r for r in load(path) if r["id"].startswith(template_id) or r["name"] == template_id), None)
    if not item: raise KeyError("template not found")
    missing = [p for p in item["parameters"] if p not in params]
    if missing: raise ValueError(f"missing parameters: {missing}")
    text = item["query"]
    for key, value in params.items(): text = text.replace("{{" + key + "}}", value)
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(text, encoding="utf-8")
    return {"template": item["name"], "language": item["language"], "output": str(output), "parameters": params}


def parse_params(values: list[str]) -> dict[str, str]:
    out = {}
    for value in values:
        if "=" not in value: raise ValueError(f"expected key=value: {value}")
        k, v = value.split("=", 1); out[k] = v
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Manage local Cypher/SPARQL query templates.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add"); add.add_argument("library"); add.add_argument("--name", required=True); add.add_argument("--language", required=True); add.add_argument("--query-file", required=True); add.add_argument("--notes", default="")
    ren = sub.add_parser("render"); ren.add_argument("library"); ren.add_argument("template_id"); ren.add_argument("--param", action="append", default=[]); ren.add_argument("--output", required=True)
    ls = sub.add_parser("list"); ls.add_argument("library")
    args = ap.parse_args()
    if args.cmd == "add": print(json.dumps(add_template(Path(args.library), args.name, args.language, Path(args.query_file), args.notes), indent=2)); return 0
    if args.cmd == "render": print(json.dumps(render(Path(args.library), args.template_id, parse_params(args.param), Path(args.output)), indent=2)); return 0
    print(json.dumps(load(Path(args.library)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
