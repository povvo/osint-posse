#!/usr/bin/env python3
"""Hashing utility / SHA-256 manifest.

Creates and verifies SHA-256 manifests for local files and folders with stable
relative paths.
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


def files_under(root: Path) -> list[Path]:
    if root.is_file(): return [root]
    if root.is_dir(): return [p for p in sorted(root.rglob("*")) if p.is_file()]
    raise FileNotFoundError(root)


def create(root: Path, output: Path) -> dict:
    files = files_under(root)
    records = [{"path": str(p), "relative_path": str(p.relative_to(root)) if root.is_dir() else p.name, "sha256": sha256(p), "bytes": p.stat().st_size} for p in files]
    manifest = {"created_utc": now(), "root": str(root), "algorithm": "sha256", "records": records}
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"output": str(output), "records": len(records)}


def verify(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = []
    for r in manifest.get("records", []):
        p = Path(r["path"])
        actual = sha256(p) if p.exists() else None
        checks.append({"path": str(p), "expected": r["sha256"], "actual": actual, "ok": actual == r["sha256"]})
    return {"manifest": str(manifest_path), "checked": len(checks), "ok": all(c["ok"] for c in checks), "checks": checks}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create or verify SHA-256 manifests.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    mk = sub.add_parser("create"); mk.add_argument("root"); mk.add_argument("--output", default="sha256_manifest.json")
    vf = sub.add_parser("verify"); vf.add_argument("manifest")
    args = ap.parse_args()
    print(json.dumps(create(Path(args.root), Path(args.output)) if args.cmd == "create" else verify(Path(args.manifest)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
