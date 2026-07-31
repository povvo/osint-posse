#!/usr/bin/env python3
"""Metadata Preservation and Web Archiving.

Creates preservation records for local web captures: URL, capture file, metadata,
hash, archive reference, and completeness notes.
"""
from __future__ import annotations
import argparse, hashlib, json, mimetypes
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def preserve(url: str, capture_file: Path, output: Path, archive_url: str = "", notes: str = "") -> dict:
    if not capture_file.exists() or not capture_file.is_file():
        raise FileNotFoundError(capture_file)
    record = {"url": url, "capture_file": str(capture_file), "archive_url": archive_url, "preserved_utc": now(), "bytes": capture_file.stat().st_size, "sha256": sha256(capture_file), "mime_guess": mimetypes.guess_type(str(capture_file))[0], "notes": notes, "completeness_review": {"headers_saved": False, "screenshots_saved": False, "linked_assets_saved": False}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a metadata preservation record for a local web capture.")
    ap.add_argument("--url", required=True)
    ap.add_argument("--capture-file", required=True)
    ap.add_argument("--archive-url", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--output", default="web_capture_preservation.json")
    args = ap.parse_args()
    print(json.dumps(preserve(args.url, Path(args.capture_file), Path(args.output), args.archive_url, args.notes), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
