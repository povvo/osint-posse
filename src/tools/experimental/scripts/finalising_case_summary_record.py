#!/usr/bin/env python3
"""Finalising the Case Summary Record.

Combines findings, actions, sources, and open issues into a final case summary
Markdown file with a JSON completion checklist.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = ["summary", "scope", "key_findings", "source_summary", "limitations", "open_issues", "handover"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_notes(path: Path) -> list[dict]:
    if not path.exists(): return []
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def collect_text(rows: list[dict], field: str, fallback: str) -> str:
    values = [str(r.get(field, "")).strip() for r in rows if str(r.get(field, "")).strip()]
    return "\n".join(f"- {v}" for v in values) if values else fallback


def finalise(case_id: str, notes: list[dict], output: Path) -> dict:
    sections = {
        "Summary": "Draft final summary.",
        "Scope": collect_text(notes, "scope", "- Scope not supplied."),
        "Key Findings": collect_text(notes, "finding", "- No findings supplied."),
        "Source Summary": collect_text(notes, "source", "- Source summary not supplied."),
        "Limitations": collect_text(notes, "limitation", "- Limitations not supplied."),
        "Open Issues": collect_text(notes, "open_issue", "- No open issues supplied."),
        "Handover": collect_text(notes, "handover", "- Handover notes not supplied."),
    }
    lines = ["# Final Case Summary Record", "", f"Case ID: {case_id}", f"Generated: {now()}", ""]
    for title, body in sections.items(): lines += [f"## {title}", "", body, ""]
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text("\n".join(lines), encoding="utf-8")
    checklist = {"case_id": case_id, "output": str(output), "completed_sections": list(sections), "ready_for_review": all(bool(v.strip()) for v in sections.values())}
    output.with_suffix(".checklist.json").write_text(json.dumps(checklist, indent=2), encoding="utf-8")
    return checklist


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a final case summary record.")
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--notes")
    ap.add_argument("--output", default="final_case_summary.md")
    args = ap.parse_args()
    print(json.dumps(finalise(args.case_id, read_notes(Path(args.notes)) if args.notes else [], Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
