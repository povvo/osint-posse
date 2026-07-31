#!/usr/bin/env python3
"""Web archive capture/search.

Compares two locally saved page captures and records archive references, changed
lines, and review notes. It does not fetch remote pages.
"""
from __future__ import annotations
import argparse, difflib, hashlib, json
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


def compare(before: Path, after: Path, output: Path, before_ref: str, after_ref: str) -> dict:
    before_lines = before.read_text(encoding="utf-8", errors="replace").splitlines()
    after_lines = after.read_text(encoding="utf-8", errors="replace").splitlines()
    diff = list(difflib.unified_diff(before_lines, after_lines, fromfile=str(before), tofile=str(after), lineterm=""))
    report = {"created_utc": now(), "before": str(before), "after": str(after), "before_sha256": sha(before), "after_sha256": sha(after), "before_archive_ref": before_ref, "after_archive_ref": after_ref, "changed": bool(diff), "diff_lines": diff[:2000]}
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return {"output": str(output), "changed": report["changed"], "diff_line_count": len(diff)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two local web archive captures.")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--before-ref", default="")
    parser.add_argument("--after-ref", default="")
    parser.add_argument("--output", default="web_archive_compare.json")
    args = parser.parse_args()
    print(json.dumps(compare(Path(args.before), Path(args.after), Path(args.output), args.before_ref, args.after_ref), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
