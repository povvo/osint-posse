#!/usr/bin/env python3
"""Slide deck software helper.

Builds a slide-by-slide Markdown outline from structured findings, preserving
source references, speaker notes, and decision asks.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(rows: list[dict], title: str, output: Path) -> dict:
    lines = [f"# {title}", "", "## Slide 1 · Bottom Line", "", "- State the BLUF.", "", "Notes: audience decision ask.", ""]
    slide_no = 2
    for row in rows:
        heading = row.get("heading") or row.get("finding") or row.get("title") or f"Evidence point {slide_no-1}"
        body = row.get("detail") or row.get("note") or row.get("finding") or ""
        source = row.get("source") or row.get("source_ref") or ""
        lines += [f"## Slide {slide_no} · {heading}", "", f"- {body}", f"- Source: {source}", "", "Notes: caveats, confidence, and likely questions.", ""]
        slide_no += 1
    lines += [f"## Slide {slide_no} · Next Actions", "", "- Decision required", "- Owner", "- Deadline", ""]
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text("\n".join(lines), encoding="utf-8")
    return {"output": str(output), "slides": slide_no}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a Markdown slide outline from findings.")
    ap.add_argument("notes"); ap.add_argument("--title", default="Briefing Deck"); ap.add_argument("--output", default="slide_deck_outline.md")
    args = ap.parse_args()
    print(json.dumps(build(read(Path(args.notes)), args.title, Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
