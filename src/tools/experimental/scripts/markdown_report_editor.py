#!/usr/bin/env python3
"""Markdown / report editor.

Builds a source-backed Markdown report from structured notes. It enforces basic
sections, flags unsupported claims, and writes a reviewer checklist.
"""
from __future__ import annotations
import argparse, csv, json, re
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_SECTIONS = ["Summary", "Scope", "Sources", "Findings", "Caveats", "Next Actions"]
CLAIM_RE = re.compile(r"\b(is|are|was|were|shows|proves|confirms|indicates)\b", re.I)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_notes(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_report(notes: list[dict], title: str, output: Path) -> dict:
    sources = sorted({str(n.get("source") or n.get("Source") or "") for n in notes if n.get("source") or n.get("Source")})
    findings = []
    warnings = []
    for i, note in enumerate(notes, 1):
        text = str(note.get("finding") or note.get("note") or note.get("text") or note)
        src = str(note.get("source") or note.get("Source") or "")
        if CLAIM_RE.search(text) and not src:
            warnings.append({"row": i, "warning": "claim-like text has no source", "text": text[:200]})
        findings.append(f"- {text}" + (f" [{src}]" if src else ""))
    lines = [f"# {title}", "", f"Generated: {now()}", ""]
    sections = {"Summary": "Draft summary goes here.", "Scope": "Define task boundaries and exclusions.", "Sources": "\n".join(f"- {s}" for s in sources) or "- No sources listed.", "Findings": "\n".join(findings) or "- No findings supplied.", "Caveats": "List confidence limits and unknowns.", "Next Actions": "List owners and follow-up items."}
    for heading in REQUIRED_SECTIONS:
        lines += [f"## {heading}", "", sections[heading], ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    check_path = output.with_suffix(".review.json")
    check_path.write_text(json.dumps({"warnings": warnings, "required_sections": REQUIRED_SECTIONS}, indent=2), encoding="utf-8")
    return {"report": str(output), "review": str(check_path), "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a structured Markdown report from notes.")
    ap.add_argument("notes")
    ap.add_argument("--title", default="Working Report")
    ap.add_argument("--output", default="report.md")
    args = ap.parse_args()
    print(json.dumps(build_report(load_notes(Path(args.notes)), args.title, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
