#!/usr/bin/env python3
"""Establishing the Operational Ontology.

Creates and validates a controlled vocabulary of entity classes, relationship
classes, aliases, and forbidden ambiguous terms.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

TERM_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 _/-]{1,80}$")


def read_terms(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def validate(rows: list[dict]) -> dict:
    findings = []
    seen = set()
    for idx, row in enumerate(rows, 1):
        term = str(row.get("term", "")).strip()
        kind = str(row.get("kind", "")).strip().lower()
        if not TERM_RE.match(term): findings.append({"row": idx, "issue": "unsafe or missing term", "term": term})
        if kind not in {"entity", "relationship", "attribute", "status"}: findings.append({"row": idx, "issue": "unknown kind", "kind": kind})
        key = (kind, term.lower())
        if key in seen: findings.append({"row": idx, "issue": "duplicate term", "term": term})
        seen.add(key)
    return {"ok": not findings, "term_count": len(rows), "findings": findings}


def export_markdown(rows: list[dict], output: Path) -> None:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(str(row.get("kind", "other")).lower(), []).append(row)
    lines = ["# Operational Ontology", ""]
    for kind, items in sorted(groups.items()):
        lines += [f"## {kind.title()}", ""]
        for item in sorted(items, key=lambda x: str(x.get("term", "")).lower()):
            lines.append(f"- **{item.get('term','')}** — {item.get('definition','')}" )
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def init_template(output: Path) -> None:
    rows = [
        {"kind": "entity", "term": "Person", "definition": "Human subject or actor", "aliases": "individual"},
        {"kind": "entity", "term": "Organisation", "definition": "Corporate, public, or informal group", "aliases": "company; body"},
        {"kind": "relationship", "term": "Controls", "definition": "Directs or materially influences", "aliases": "owns; manages"},
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["kind", "term", "definition", "aliases"])
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or validate an operational ontology CSV.")
    ap.add_argument("--init")
    ap.add_argument("--validate")
    ap.add_argument("--markdown")
    args = ap.parse_args()
    if args.init:
        init_template(Path(args.init)); print(json.dumps({"created": args.init}, indent=2)); return 0
    if not args.validate:
        ap.error("use --init or --validate")
    rows = read_terms(Path(args.validate)); result = validate(rows)
    if args.markdown: export_markdown(rows, Path(args.markdown)); result["markdown"] = args.markdown
    print(json.dumps(result, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
