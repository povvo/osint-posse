#!/usr/bin/env python3
"""Meta-Log and Audit Trail Setup.

Creates an append-only operational meta-log for actions, file changes, decisions,
and validation events. Exports JSONL and Markdown summaries.
"""
from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

EVENTS = {"action", "decision", "file_change", "validation", "handoff", "note"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append(log: Path, event: str, actor: str, detail: str, ref: str = "") -> dict:
    if event not in EVENTS: raise ValueError(f"event must be one of {sorted(EVENTS)}")
    log.parent.mkdir(parents=True, exist_ok=True)
    row = {"event_id": str(uuid.uuid4()), "time_utc": now(), "event": event, "actor": actor, "detail": detail, "ref": ref}
    with log.open("a", encoding="utf-8") as handle: handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    write_markdown(log)
    return row


def rows(log: Path) -> list[dict]:
    if not log.exists(): return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_markdown(log: Path) -> None:
    lines = ["# Meta-Log / Audit Trail", ""]
    for row in rows(log):
        lines.append(f"- `{row['time_utc']}` **{row['event']}** by {row['actor']}: {row['detail']} ({row.get('ref','')})")
    log.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Append to or inspect a meta-log audit trail.")
    ap.add_argument("log")
    ap.add_argument("--event", choices=sorted(EVENTS))
    ap.add_argument("--actor", default="analyst")
    ap.add_argument("--detail")
    ap.add_argument("--ref", default="")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(); path = Path(args.log)
    if args.list: print(json.dumps(rows(path), indent=2)); return 0
    if not args.event or not args.detail: ap.error("--event and --detail are required unless --list is used")
    print(json.dumps(append(path, args.event, args.actor, args.detail, args.ref), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
