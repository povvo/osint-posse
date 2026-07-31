#!/usr/bin/env python3
"""database/subject-profiles.md.

Creates a subject profile Markdown record and matching JSON shell for structured
profile data, source references, caveats, and unresolved questions.
"""
from __future__ import annotations
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path

SECTIONS = ["Identity", "Known Attributes", "Associations", "Timeline", "Source References", "Confidence and Caveats", "Open Questions"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip()).strip("_")
    return cleaned[:90] or "subject"


def create_profile(subject_id: str, label: str, output_dir: Path, subject_type: str = "unknown") -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_filename(subject_id)
    md_path = output_dir / f"{stem}.md"
    json_path = output_dir / f"{stem}.json"
    lines = [f"# Subject Profile: {label}", "", f"Subject ID: {subject_id}", f"Type: {subject_type}", f"Created: {now()}", ""]
    for section in SECTIONS:
        lines += [f"## {section}", "", "- ", ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    data = {"subject_id": subject_id, "label": label, "type": subject_type, "created_at_utc": now(), "attributes": {}, "associations": [], "timeline": [], "source_refs": [], "caveats": [], "open_questions": []}
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"markdown": str(md_path), "json": str(json_path), "subject_id": subject_id}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a subject profile Markdown/JSON pair.")
    ap.add_argument("--subject-id", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--type", default="unknown")
    ap.add_argument("--output-dir", default="subject_profiles")
    args = ap.parse_args()
    print(json.dumps(create_profile(args.subject_id, args.label, Path(args.output_dir), args.type), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
