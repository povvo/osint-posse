#!/usr/bin/env python3
"""InVID/WeVerify-style video verification.

Maintains a local video verification worksheet: frame path, thumbnail hash,
metadata notes, reuse check notes, and reviewer status.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["video_id", "time_utc", "video_file", "frame_file", "frame_sha256", "metadata_notes", "thumbnail_notes", "reuse_notes", "status", "reviewer"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    if not path.exists() or not path.is_file(): return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)


def add(log: Path, video_file: str, frame_file: str, metadata_notes: str, thumbnail_notes: str, reuse_notes: str, reviewer: str) -> dict:
    rows = read(log)
    row = {"video_id": str(uuid.uuid4()), "time_utc": now(), "video_file": video_file, "frame_file": frame_file, "frame_sha256": sha256(Path(frame_file)) if frame_file else "", "metadata_notes": metadata_notes, "thumbnail_notes": thumbnail_notes, "reuse_notes": reuse_notes, "status": "pending", "reviewer": reviewer}
    rows.append(row); write(log, rows); return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Maintain a local video verification log.")
    parser.add_argument("log")
    parser.add_argument("--video-file", required=True)
    parser.add_argument("--frame-file", default="")
    parser.add_argument("--metadata-notes", default="")
    parser.add_argument("--thumbnail-notes", default="")
    parser.add_argument("--reuse-notes", default="")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(); path = Path(args.log)
    if args.list:
        print(json.dumps(read(path), indent=2)); return 0
    print(json.dumps(add(path, args.video_file, args.frame_file, args.metadata_notes, args.thumbnail_notes, args.reuse_notes, args.reviewer), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
