#!/usr/bin/env python3
"""Case notebook / decision log.

Append structured decisions, assumptions, scope changes, and negative results to a
case notebook stored as JSONL plus a readable Markdown index.
"""
from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

KINDS = {"decision", "assumption", "scope_change", "negative_result", "question", "note"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append_record(folder: Path, kind: str, text: str, actor: str, source: str = "", tags: list[str] | None = None) -> dict:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of: {', '.join(sorted(KINDS))}")
    folder.mkdir(parents=True, exist_ok=True)
    record = {"id": str(uuid.uuid4()), "created_at_utc": now(), "kind": kind, "actor": actor, "text": text, "source": source, "tags": tags or []}
    with (folder / "decision_log.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    rebuild_markdown(folder)
    return record


def read_records(folder: Path) -> list[dict]:
    path = folder / "decision_log.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rebuild_markdown(folder: Path) -> None:
    rows = read_records(folder)
    lines = ["# Case Notebook / Decision Log", "", f"Updated: {now()}", ""]
    for row in rows:
        tags = ", ".join(row.get("tags", []))
        lines += [f"## {row['kind']} · {row['created_at_utc']}", "", row["text"], "", f"- Actor: {row['actor']}", f"- Source: {row.get('source','')}", f"- Tags: {tags}", ""]
    (folder / "decision_log.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Append or list case notebook records.")
    ap.add_argument("folder")
    ap.add_argument("--kind", choices=sorted(KINDS))
    ap.add_argument("--text")
    ap.add_argument("--actor", default="analyst")
    ap.add_argument("--source", default="")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    folder = Path(args.folder)
    if args.list:
        print(json.dumps(read_records(folder), indent=2, ensure_ascii=False)); return 0
    if not args.kind or not args.text:
        ap.error("--kind and --text are required unless --list is used")
    print(json.dumps(append_record(folder, args.kind, args.text, args.actor, args.source, args.tag), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
