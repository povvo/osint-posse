#!/usr/bin/env python3
"""Timeline artefact parser.

Parses local text, CSV, JSON, and JSONL artefacts for timestamp-like values and
emits a normalised event CSV for chronology review.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

TIME_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ][0-2]\d:[0-5]\d(?::[0-5]\d)?)?Z?\b")
FIELDS = ["source_file", "line_or_row", "timestamp_raw", "context"]


def parse_text(path: Path) -> list[dict]:
    events = []
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for match in TIME_RE.finditer(line):
            events.append({"source_file": str(path), "line_or_row": number, "timestamp_raw": match.group(0), "context": line[:500]})
    return events


def parse_csv(path: Path) -> list[dict]:
    events = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for number, row in enumerate(csv.DictReader(handle), 1):
            text = " ".join(str(value) for value in row.values() if value)
            for match in TIME_RE.finditer(text):
                events.append({"source_file": str(path), "line_or_row": number, "timestamp_raw": match.group(0), "context": text[:500]})
    return events


def parse_json(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    events = []
    for match in TIME_RE.finditer(text):
        events.append({"source_file": str(path), "line_or_row": "json", "timestamp_raw": match.group(0), "context": text[max(0, match.start()-120):match.end()+120]})
    return events


def parse_files(paths: list[Path], output: Path) -> dict:
    events = []
    for path in paths:
        if path.suffix.lower() == ".csv": events.extend(parse_csv(path))
        elif path.suffix.lower() in {".json", ".jsonl"}: events.extend(parse_json(path))
        else: events.extend(parse_text(path))
    events.sort(key=lambda row: row["timestamp_raw"])
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(events)
    return {"output": str(output), "events": len(events)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse local artefacts for timestamped events.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--output", default="timeline_artifacts.csv")
    args = parser.parse_args()
    print(json.dumps(parse_files([Path(p) for p in args.paths], Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
