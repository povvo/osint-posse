#!/usr/bin/env python3
"""SIEM / log search.

Searches local log files for terms, time windows, and field patterns. Outputs a
CSV of matching lines with file, line number, timestamp guess, and context.
"""
from __future__ import annotations
import argparse, csv, re, json
from pathlib import Path

TIME_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}[T ][0-2]\d:[0-5]\d(?::[0-5]\d)?Z?\b")


def iter_files(paths: list[Path]) -> list[Path]:
    files = []
    for path in paths:
        if path.is_file(): files.append(path)
        elif path.is_dir(): files.extend(p for p in sorted(path.rglob("*")) if p.is_file())
    return files


def search(paths: list[Path], pattern: str, ignore_case: bool, output: Path) -> dict:
    flags = re.I if ignore_case else 0
    regex = re.compile(pattern, flags)
    results = []
    for file in iter_files(paths):
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception as exc:
            results.append({"file": str(file), "line": 0, "timestamp": "", "match": "", "context": f"read error: {exc}"})
            continue
        for idx, line in enumerate(lines, 1):
            if regex.search(line):
                ts = TIME_RE.search(line)
                results.append({"file": str(file), "line": idx, "timestamp": ts.group(0) if ts else "", "match": regex.search(line).group(0), "context": line[:1000]})
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "line", "timestamp", "match", "context"])
        writer.writeheader(); writer.writerows(results)
    return {"output": str(output), "matches": len(results), "files_searched": len(iter_files(paths))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Search local log files and export matching rows.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--case-sensitive", action="store_true")
    parser.add_argument("--output", default="log_search_results.csv")
    args = parser.parse_args()
    print(json.dumps(search([Path(p) for p in args.paths], args.pattern, not args.case_sensitive, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
