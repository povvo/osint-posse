#!/usr/bin/env python3
"""Mandatory Source Summary Statement.

Builds a concise source summary from a source register, including source count,
reliability spread, credibility spread, and caveats.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path


def read(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data, list) else data.get("records", [data])
    with path.open(newline="", encoding="utf-8-sig") as handle: return list(csv.DictReader(handle))


def build(rows: list[dict], output: Path) -> dict:
    reliability = Counter(str(r.get("reliability", "unknown") or "unknown") for r in rows)
    credibility = Counter(str(r.get("credibility", "unknown") or "unknown") for r in rows)
    source_types = Counter(str(r.get("source_type", "unknown") or "unknown") for r in rows)
    caveats = []
    if reliability.get("F", 0): caveats.append("Some source reliability cannot be judged.")
    if credibility.get("6", 0): caveats.append("Some information credibility cannot be judged.")
    text = ["# Source Summary Statement", "", f"Sources reviewed: {len(rows)}", "", "## Source types", *[f"- {k}: {v}" for k, v in source_types.items()], "", "## Reliability", *[f"- {k}: {v}" for k, v in reliability.items()], "", "## Credibility", *[f"- {k}: {v}" for k, v in credibility.items()], "", "## Caveats", *(f"- {c}" for c in caveats or ["No automatic caveats detected."])]
    output.write_text("\n".join(text) + "\n", encoding="utf-8")
    return {"output": str(output), "source_count": len(rows), "caveats": caveats}


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a mandatory source summary statement.")
    ap.add_argument("source_register"); ap.add_argument("--output", default="source_summary_statement.md")
    args = ap.parse_args()
    print(json.dumps(build(read(Path(args.source_register)), Path(args.output)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
