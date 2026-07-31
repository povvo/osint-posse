#!/usr/bin/env python3
"""Subject and Corporate Profiles.

Merges subject and company CSV rows into a profile bundle with identifiers,
relationships, source references, and unresolved gaps.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def first(row: dict, names: list[str]) -> str:
    lower = {k.lower(): k for k in row}
    for name in names:
        key = lower.get(name.lower())
        if key and str(row.get(key, "")).strip(): return str(row[key]).strip()
    return ""


def build_profiles(subject_csv: Path, company_csv: Path, output: Path) -> dict:
    subjects = read_csv(subject_csv) if subject_csv else []
    companies = read_csv(company_csv) if company_csv else []
    profiles = {"created_at_utc": now(), "subjects": [], "companies": [], "relationships": [], "gaps": []}
    for row in subjects:
        sid = first(row, ["subject_id", "id", "person_id"]) or f"subject_{len(profiles['subjects'])+1}"
        profiles["subjects"].append({"id": sid, "name": first(row, ["name", "label", "person"]), "identifiers": {k: v for k, v in row.items() if "id" in k.lower() and v}, "source_ref": first(row, ["source", "source_ref"]), "raw": row})
    for row in companies:
        cid = first(row, ["company_id", "organisation_id", "id"]) or f"company_{len(profiles['companies'])+1}"
        profiles["companies"].append({"id": cid, "name": first(row, ["company", "organisation", "name", "label"]), "jurisdiction": first(row, ["jurisdiction", "country"]), "source_ref": first(row, ["source", "source_ref"]), "raw": row})
    company_names = {c["name"].lower(): c["id"] for c in profiles["companies"] if c["name"]}
    for subject in profiles["subjects"]:
        employer = first(subject["raw"], ["company", "organisation", "employer"])
        if employer and employer.lower() in company_names:
            profiles["relationships"].append({"source": subject["id"], "target": company_names[employer.lower()], "type": "associated_with"})
        elif employer:
            profiles["gaps"].append({"subject": subject["id"], "missing_company_record": employer})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(profiles, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"output": str(output), "subjects": len(profiles["subjects"]), "companies": len(profiles["companies"]), "relationships": len(profiles["relationships"]), "gaps": len(profiles["gaps"])}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build subject and corporate profile bundle.")
    ap.add_argument("--subjects", required=True)
    ap.add_argument("--companies", required=True)
    ap.add_argument("--output", default="profiles_bundle.json")
    args = ap.parse_args()
    print(json.dumps(build_profiles(Path(args.subjects), Path(args.companies), Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
