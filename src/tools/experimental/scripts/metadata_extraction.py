#!/usr/bin/env python3
"""EXIFTool / metadata extraction.

Extracts local file metadata available through the standard library and writes a
CSV/JSON report. Optional EXIFTool output can be imported as JSON for review.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, mimetypes, os
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["path", "name", "suffix", "bytes", "sha256", "modified_utc", "created_utc", "mime_guess"]


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def describe(path: Path) -> dict:
    stat = path.stat()
    return {"path": str(path), "name": path.name, "suffix": path.suffix.lower(), "bytes": stat.st_size, "sha256": sha256(path), "modified_utc": iso(stat.st_mtime), "created_utc": iso(stat.st_ctime), "mime_guess": mimetypes.guess_type(str(path))[0] or ""}


def collect(paths: list[Path]) -> list[dict]:
    out = []
    for path in paths:
        if path.is_file(): out.append(describe(path))
        elif path.is_dir(): out.extend(describe(p) for p in sorted(path.rglob("*")) if p.is_file())
    return out


def export(rows: list[dict], csv_out: Path, json_out: Path) -> dict:
    with csv_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    json_out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return {"csv": str(csv_out), "json": str(json_out), "records": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract local file metadata to CSV and JSON.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--csv-output", default="metadata_report.csv")
    parser.add_argument("--json-output", default="metadata_report.json")
    args = parser.parse_args()
    print(json.dumps(export(collect([Path(p) for p in args.paths]), Path(args.csv_output), Path(args.json_output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
