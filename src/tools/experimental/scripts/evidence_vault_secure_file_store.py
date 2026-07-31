#!/usr/bin/env python3
"""Evidence vault / secure file store.

Copies local files into a case vault, records SHA-256 hashes, and maintains an
append-only custody ledger. No deletion or network activity is performed.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, uuid
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)
    return cleaned.strip("._-") or "file"


def ledger_path(vault: Path) -> Path:
    return vault / "vault_ledger.jsonl"


def append_ledger(vault: Path, event: dict) -> None:
    with ledger_path(vault).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def ingest(vault: Path, source: Path, handler: str, note: str = "") -> dict:
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(source)
    vault.mkdir(parents=True, exist_ok=True)
    file_id = str(uuid.uuid4())
    original_hash = digest(source)
    stored_name = f"{file_id}_{safe_name(source.name)}"
    stored_path = vault / "objects" / stored_name
    stored_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, stored_path)
    stored_hash = digest(stored_path)
    if original_hash != stored_hash:
        stored_path.unlink(missing_ok=True)
        raise RuntimeError("hash mismatch after copy")
    record = {"event": "ingest", "id": file_id, "time_utc": now(), "handler": handler, "source_path": str(source), "stored_path": str(stored_path), "sha256": stored_hash, "bytes": stored_path.stat().st_size, "note": note}
    append_ledger(vault, record)
    return record


def list_ledger(vault: Path) -> list[dict]:
    path = ledger_path(vault)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def verify(vault: Path) -> dict:
    rows = list_ledger(vault); checks = []
    for row in rows:
        if row.get("event") != "ingest":
            continue
        path = Path(row["stored_path"])
        actual = digest(path) if path.exists() else None
        checks.append({"id": row["id"], "path": str(path), "exists": path.exists(), "expected_sha256": row["sha256"], "actual_sha256": actual, "ok": actual == row["sha256"]})
    return {"vault": str(vault), "checked": len(checks), "ok": all(c["ok"] for c in checks), "checks": checks}


def main() -> int:
    ap = argparse.ArgumentParser(description="Local file vault with SHA-256 ledger.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ing = sub.add_parser("ingest"); ing.add_argument("vault"); ing.add_argument("source"); ing.add_argument("--handler", required=True); ing.add_argument("--note", default="")
    ls = sub.add_parser("list"); ls.add_argument("vault")
    vf = sub.add_parser("verify"); vf.add_argument("vault")
    args = ap.parse_args()
    if args.cmd == "ingest": print(json.dumps(ingest(Path(args.vault), Path(args.source), args.handler, args.note), indent=2)); return 0
    if args.cmd == "list": print(json.dumps(list_ledger(Path(args.vault)), indent=2)); return 0
    print(json.dumps(verify(Path(args.vault)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
