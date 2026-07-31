#!/usr/bin/env python3
"""Leeds method / cluster worksheet.

Builds a cluster worksheet for match rows by assigning coloured cluster labels
from shared-match group keys and producing review-ready CSV output.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path

COLOURS = ["blue", "green", "yellow", "pink", "purple", "orange", "grey", "brown"]


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def cluster(rows: list[dict], key_col: str, output: Path) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(key_col, "unassigned") or "unassigned")].append(row)
    out = []
    for idx, (key, items) in enumerate(sorted(groups.items()), 1):
        colour = COLOURS[(idx - 1) % len(COLOURS)]
        for item in items:
            out.append({**item, "leeds_cluster": key, "cluster_colour": colour, "candidate_branch": "", "review_notes": ""})
    fields = sorted({k for row in out for k in row}) if out else ["leeds_cluster"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(out)
    return {"output": str(output), "clusters": len(groups), "rows": len(out)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Leeds-method cluster worksheet.")
    parser.add_argument("matches_csv")
    parser.add_argument("--key-col", default="shared_group")
    parser.add_argument("--output", default="leeds_cluster_worksheet.csv")
    args = parser.parse_args()
    print(json.dumps(cluster(read(Path(args.matches_csv)), args.key_col, Path(args.output)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
