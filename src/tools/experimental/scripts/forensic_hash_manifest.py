#!/usr/bin/env python3
"""Forensic hash manifest.

Records hashes, acquisition path, acquisition time, analyst, and tool version for
local files. It can verify the manifest later against the same paths.
"""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "1.0"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_manifest(paths: list[Path], output: Path, analyst: str) -> dict:
    records = []
    for path in paths:
        candidates = [path] if path.is_file() else [p for p in sorted(path.rglob("*")) if p.is_file()] if path.is_dir() else []
        if not candidates:
            records.append({"path": str(path), "exists": False})
        for item in candidates:
            records.append({"path": str(item), "exists": True, "sha256": sha256(item), "bytes": item.stat().st_size, "acquired_utc": now(), "analyst": analyst, "tool_version": TOOL_VERSION})
    manifest = {"created_utc": now(), "algorithm": "sha256", "records": records}
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"output": str(output), "records": len(records)}


def verify(manifest: Path) -> dict:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    checks = []
    for row in data.get("records", []):
        path = Path(row["path"])
        actual = sha256(path) if path.exists() and path.is_file() else None
        checks.append({"path": str(path), "ok": actual == row.get("sha256"), "expected": row.get("sha256"), "actual": actual})
    return {"checked": len(checks), "ok": all(item["ok"] for item in checks), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or verify a local hash manifest.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    mk = sub.add_parser("make"); mk.add_argument("paths", nargs="+"); mk.add_argument("--output", default="forensic_hash_manifest.json"); mk.add_argument("--analyst", default="analyst")
    vf = sub.add_parser("verify"); vf.add_argument("manifest")
    args = parser.parse_args()
    result = make_manifest([Path(p) for p in args.paths], Path(args.output), args.analyst) if args.cmd == "make" else verify(Path(args.manifest))
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
