#!/usr/bin/env python3
"""evidence_preservation.py.

Preserves local evidence metadata by hashing files, recording acquisition context,
and writing a manifest with stable item IDs.
"""
from __future__ import annotations
import argparse, hashlib, json, mimetypes, uuid
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


def preserve(paths: list[Path], output: Path, acquired_by: str, source_ref: str, note: str) -> dict:
    records = []
    for path in paths:
        record = {"item_id": str(uuid.uuid4()), "path": str(path), "exists": path.exists(), "acquired_at_utc": now(), "acquired_by": acquired_by, "source_ref": source_ref, "note": note}
        if path.exists() and path.is_file():
            record.update({"bytes": path.stat().st_size, "sha256": sha256(path), "mime_guess": mimetypes.guess_type(str(path))[0]})
        records.append(record)
    manifest = {"created_at_utc": now(), "record_count": len(records), "records": records}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"manifest": str(output), "record_count": len(records), "missing": [r["path"] for r in records if not r["exists"]]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a local evidence preservation manifest.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--output", default="evidence_preservation_manifest.json")
    ap.add_argument("--acquired-by", default="analyst")
    ap.add_argument("--source-ref", default="")
    ap.add_argument("--note", default="")
    args = ap.parse_args()
    print(json.dumps(preserve([Path(p) for p in args.files], Path(args.output), args.acquired_by, args.source_ref, args.note), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
