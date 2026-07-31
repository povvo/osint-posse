#!/usr/bin/env python3
"""GEDCOM editor / Gramps helper.

Parses basic GEDCOM individual and family records into CSV summaries for review
before editing in a genealogy database tool.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

INDI_RE = re.compile(r"^0 @([^@]+)@ INDI")
FAM_RE = re.compile(r"^0 @([^@]+)@ FAM")


def parse(path: Path) -> dict:
    people = []
    families = []
    current = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if match := INDI_RE.match(line):
            current = {"id": match.group(1), "name": "", "birth": "", "death": ""}
            people.append(current)
        elif match := FAM_RE.match(line):
            current = {"id": match.group(1), "husband": "", "wife": "", "children": []}
            families.append(current)
        elif current is not None:
            parts = line.split(" ", 2)
            if len(parts) >= 3 and parts[1] == "NAME" and "name" in current: current["name"] = parts[2]
            if len(parts) >= 3 and parts[1] == "HUSB" and "husband" in current: current["husband"] = parts[2]
            if len(parts) >= 3 and parts[1] == "WIFE" and "wife" in current: current["wife"] = parts[2]
            if len(parts) >= 3 and parts[1] == "CHIL" and "children" in current: current["children"].append(parts[2])
    return {"people": people, "families": families}


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def export(gedcom: Path, output_dir: Path) -> dict:
    data = parse(gedcom)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "gedcom_people.csv", data["people"], ["id", "name", "birth", "death"])
    fam_rows = [{**f, "children": ";".join(f["children"])} for f in data["families"]]
    write_csv(output_dir / "gedcom_families.csv", fam_rows, ["id", "husband", "wife", "children"])
    return {"people": len(data["people"]), "families": len(data["families"]), "output_dir": str(output_dir)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export basic GEDCOM summaries to CSV.")
    parser.add_argument("gedcom"); parser.add_argument("--output-dir", default="gedcom_export")
    args = parser.parse_args()
    print(json.dumps(export(Path(args.gedcom), Path(args.output_dir)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
