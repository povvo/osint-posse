#!/usr/bin/env python3
"""Digital Evidence Hashing.

Calculates SHA-256 hashes for files or directories and verifies later manifests.
Includes file size and modification time for acquisition review.
"""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def hash_file(path: Path) -> dict:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    stat = path.stat()
    return {"path": str(path), "sha256": h.hexdigest(), "bytes": stat.st_size, "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")}


def collect(paths: list[Path]) -> list[dict]:
    records = []
    for path in paths:
        if path.is_file(): records.append(hash_file(path))
        elif path.is_dir(): records.extend(hash_file(p) for p in sorted(path.rglob("*")) if p.is_file())
        else: records.append({"path": str(path), "error": "not found"})
    return records


def write_manifest(paths: list[Path], output: Path) -> dict:
    manifest = {"created_utc": now(), "algorithm": "sha256", "records": collect(paths)}
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"output": str(output), "records": len(manifest["records"])}


def verify(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = []
    for record in manifest.get("records", []):
        path = Path(record["path"])
        if not path.exists(): checks.append({**record, "ok": False, "actual": None}); continue
        actual = hash_file(path)["sha256"]
        checks.append({"path": str(path), "expected": record.get("sha256"), "actual": actual, "ok": actual == record.get("sha256")})
    return {"manifest": str(manifest_path), "checked": len(checks), "ok": all(c["ok"] for c in checks), "checks": checks}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or verify SHA-256 file manifests.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    mk = sub.add_parser("make"); mk.add_argument("paths", nargs="+"); mk.add_argument("--output", default="sha256_manifest.json")
    vf = sub.add_parser("verify"); vf.add_argument("manifest")
    args = ap.parse_args()
    if args.cmd == "make": print(json.dumps(write_manifest([Path(p) for p in args.paths], Path(args.output)), indent=2)); return 0
    print(json.dumps(verify(Path(args.manifest)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
