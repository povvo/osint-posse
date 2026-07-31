#!/usr/bin/env python3
"""Plaso / log2timeline manifest helper.

Prepares local filesystem and log artefact manifests for later timeline tooling.
It records paths, sizes, hashes, and intended parser hints without running Plaso.
"""
from __future__ import annotations
import argparse, hashlib, json
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


def parser_hint(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".evtx", ".evt"}: return "windows_event_log"
    if suffix in {".log", ".txt"}: return "text_log"
    if suffix in {".json", ".jsonl"}: return "json_log"
    if suffix in {".sqlite", ".db"}: return "sqlite_artifact"
    return "auto"


def build(inputs: list[Path], output: Path, analyst: str) -> dict:
    files = []
    for root in inputs:
        if root.is_file(): candidates = [root]
        elif root.is_dir(): candidates = [p for p in sorted(root.rglob("*")) if p.is_file()]
        else:
            files.append({"path": str(root), "error": "not found"}); continue
        for path in candidates:
            files.append({"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path), "parser_hint": parser_hint(path)})
    manifest = {"created_utc": now(), "analyst": analyst, "tooling_target": "plaso/log2timeline", "file_count": len(files), "files": files}
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"output": str(output), "file_count": len(files)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a manifest for Plaso/log2timeline input artefacts.")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", default="log2timeline_input_manifest.json")
    parser.add_argument("--analyst", default="analyst")
    args = parser.parse_args()
    print(json.dumps(build([Path(p) for p in args.inputs], Path(args.output), args.analyst), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
