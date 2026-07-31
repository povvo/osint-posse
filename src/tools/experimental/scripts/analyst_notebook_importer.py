#!/usr/bin/env python3
"""IBM i2 Analyst's Notebook import helper.

Creates clean entity and link CSV exports suitable for import into link-analysis
notebook tools. It validates required IDs and relationship labels locally.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

ENTITY_FIELDS = ["entity_id", "entity_type", "label", "description", "source_ref"]
LINK_FIELDS = ["from_id", "to_id", "relationship", "source_ref", "confidence"]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def build(entity_csv: Path, edge_csv: Path, output_dir: Path) -> dict:
    entities = read_csv(entity_csv); edges = read_csv(edge_csv)
    entity_rows, link_rows, findings = [], [], []
    known = set()
    for i, row in enumerate(entities, 1):
        eid = row.get("entity_id") or row.get("id") or row.get("label")
        if not eid: findings.append({"file": str(entity_csv), "row": i, "issue": "missing entity id"}); continue
        known.add(eid)
        entity_rows.append({"entity_id": eid, "entity_type": row.get("entity_type") or row.get("type") or "Entity", "label": row.get("label") or eid, "description": row.get("description", ""), "source_ref": row.get("source_ref", "")})
    for i, row in enumerate(edges, 1):
        src = row.get("from_id") or row.get("source"); dst = row.get("to_id") or row.get("target")
        if not src or not dst: findings.append({"file": str(edge_csv), "row": i, "issue": "missing link endpoint"}); continue
        if src not in known or dst not in known: findings.append({"file": str(edge_csv), "row": i, "issue": "link endpoint absent from entity table"})
        link_rows.append({"from_id": src, "to_id": dst, "relationship": row.get("relationship") or row.get("type") or "related_to", "source_ref": row.get("source_ref", ""), "confidence": row.get("confidence", "low")})
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "notebook_entities.csv", entity_rows, ENTITY_FIELDS)
    write_csv(output_dir / "notebook_links.csv", link_rows, LINK_FIELDS)
    return {"entities": len(entity_rows), "links": len(link_rows), "findings": findings, "output_dir": str(output_dir)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare entity/link CSVs for analyst notebook import.")
    ap.add_argument("--entities", required=True); ap.add_argument("--edges", required=True); ap.add_argument("--output-dir", default="notebook_import")
    args = ap.parse_args()
    print(json.dumps(build(Path(args.entities), Path(args.edges), Path(args.output_dir)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
