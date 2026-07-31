#!/usr/bin/env python3
"""Data catalog / schema registry.

Registers datasets, owners, fields, sensitivity labels, and retention notes in a
JSON catalog with Markdown export.
"""
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

LABELS = {"public", "internal", "restricted", "sensitive"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict:
    if not path.exists():
        return {"datasets": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, catalog: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    export_md(path.with_suffix(".md"), catalog)


def infer_fields(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        headers = reader.fieldnames or []
    fields = []
    for header in headers:
        values = [r.get(header, "") for r in rows]
        fields.append({"name": header, "non_empty": sum(1 for v in values if v), "sample": [v for v in values if v][:3], "description": "", "sensitivity": "internal"})
    return fields


def register(catalog_path: Path, name: str, owner: str, locator: str, label: str, csv_sample: str | None, retention: str) -> dict:
    if label not in LABELS:
        raise ValueError(f"label must be one of {sorted(LABELS)}")
    catalog = load(catalog_path)
    dataset = {"id": str(uuid.uuid4()), "name": name, "owner": owner, "locator": locator, "label": label, "retention": retention, "registered_at_utc": now(), "fields": infer_fields(Path(csv_sample)) if csv_sample else []}
    catalog["datasets"].append(dataset)
    save(catalog_path, catalog)
    return dataset


def export_md(path: Path, catalog: dict) -> None:
    lines = ["# Data Catalog", ""]
    for item in catalog.get("datasets", []):
        lines += [f"## {item['name']}", "", f"- ID: {item['id']}", f"- Owner: {item['owner']}", f"- Locator: {item['locator']}", f"- Label: {item['label']}", f"- Retention: {item['retention']}", "", "### Fields", ""]
        for field in item.get("fields", []):
            lines.append(f"- `{field['name']}` · {field['sensitivity']} · non-empty {field['non_empty']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Maintain a JSON data catalog and schema registry.")
    ap.add_argument("catalog")
    ap.add_argument("--name")
    ap.add_argument("--owner")
    ap.add_argument("--locator")
    ap.add_argument("--label", choices=sorted(LABELS), default="internal")
    ap.add_argument("--sample-csv")
    ap.add_argument("--retention", default="unspecified")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    path = Path(args.catalog)
    if args.list:
        print(json.dumps(load(path), indent=2)); return 0
    for key in ("name", "owner", "locator"):
        if not getattr(args, key): ap.error(f"--{key.replace('_','-')} is required")
    print(json.dumps(register(path, args.name, args.owner, args.locator, args.label, args.sample_csv, args.retention), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
