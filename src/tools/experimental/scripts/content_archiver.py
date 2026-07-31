#!/usr/bin/env python3
"""content_archiver.py.

Archives local files into a case folder, computes hashes, records source paths,
and writes a manifest. Network capture is intentionally not performed here.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil
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


def unique_target(folder: Path, name: str) -> Path:
    target = folder / name
    if not target.exists(): return target
    stem, suffix = target.stem, target.suffix
    i = 2
    while True:
        candidate = folder / f"{stem}_{i}{suffix}"
        if not candidate.exists(): return candidate
        i += 1


def archive(items: list[Path], output_dir: Path, note: str = "") -> dict:
    objects = output_dir / "objects"; objects.mkdir(parents=True, exist_ok=True)
    records = []
    for item in items:
        if item.is_dir():
            files = [p for p in sorted(item.rglob("*")) if p.is_file()]
        elif item.is_file():
            files = [item]
        else:
            records.append({"source": str(item), "error": "not found"}); continue
        for src in files:
            dst = unique_target(objects, src.name)
            shutil.copy2(src, dst)
            records.append({"source": str(src), "archive_path": str(dst), "sha256": sha256(dst), "bytes": dst.stat().st_size, "archived_utc": now(), "note": note})
    manifest = {"created_utc": now(), "records": records}
    (output_dir / "archive_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"output_dir": str(output_dir), "records": len(records)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Archive local content with SHA-256 manifest.")
    ap.add_argument("items", nargs="+")
    ap.add_argument("--output-dir", default="content_archive")
    ap.add_argument("--note", default="")
    args = ap.parse_args()
    print(json.dumps(archive([Path(p) for p in args.items], Path(args.output_dir), args.note), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
