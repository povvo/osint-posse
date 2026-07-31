#!/usr/bin/env python3
"""Evidence Vault Archiving.

Packages a local evidence vault into an archive manifest with hashes, object
counts, and a release checklist. It does not delete or compress originals.
"""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def archive_manifest(vault: Path, output: Path, archive_id: str, prepared_by: str) -> dict:
    if not vault.exists() or not vault.is_dir(): raise FileNotFoundError(vault)
    files = [p for p in sorted(vault.rglob("*")) if p.is_file()]
    records = [{"relative_path": str(p.relative_to(vault)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files]
    manifest = {"archive_id": archive_id, "vault": str(vault), "prepared_by": prepared_by, "created_utc": now(), "file_count": len(records), "total_bytes": sum(r["bytes"] for r in records), "records": records, "release_checklist": {"hashes_verified": False, "handling_reviewed": False, "recipient_authorised": False}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"output": str(output), "file_count": len(records), "total_bytes": manifest["total_bytes"]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Create an archive manifest for a local evidence vault.")
    ap.add_argument("vault"); ap.add_argument("--output", default="evidence_vault_archive_manifest.json"); ap.add_argument("--archive-id", required=True); ap.add_argument("--prepared-by", default="analyst")
    args = ap.parse_args()
    print(json.dumps(archive_manifest(Path(args.vault), Path(args.output), args.archive_id, args.prepared_by), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
