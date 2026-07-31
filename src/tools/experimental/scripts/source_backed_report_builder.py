#!/usr/bin/env python3
"""Source-backed report builder.

Assembles a Markdown report from finding rows and enforces that each finding has
a source reference and confidence statement.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(rows: list[dict], title: str, output: Path) -> dict:
    warnings = []
    lines = [f"# {title}", "", "## Findings", ""]
    for i, row in enumerate(rows, 1):
        finding = row.get("finding") or row.get("claim") or row.get("note") or ""
        source = row.get("source_ref") or row.get("source") or ""
        confidence = row.get("confidence") or ""
        if not source: warnings.append({"row": i, "issue": "missing source reference"})
        if not confidence: warnings.append({"row": i, "issue": "missing confidence"})
        lines += [f"### Finding {i}", "", finding, "", f"- Source: {source}", f"- Confidence: {confidence or 'not stated'}", ""]
    lines += ["## Caveats", "", "- Review all warnings before dissemination.", ""]
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text("\n".join(lines), encoding="utf-8")
    output.with_suffix(".review.json").write_text(json.dumps({"warnings": warnings}, indent=2), encoding="utf-8")
    return {"output": str(output), "findings": len(rows), "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a source-backed Markdown report.")
    ap.add_argument("findings"); ap.add_argument("--title", default="Source-Backed Report"); ap.add_argument("--output", default="source_backed_report.md")
    args = ap.parse_args()
    print(json.dumps(build(read(Path(args.findings)), args.title, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
