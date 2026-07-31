#!/usr/bin/env python3
"""DNA match platform / clustering tool.

Creates cluster worksheets for consented DNA-match work. It groups matches by
shared segment group or manual cluster key and records evidence limits.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def cluster(rows: list[dict], key_col: str) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        key = str(row.get(key_col, "unassigned") or "unassigned")
        groups[key].append(row)
    return {"cluster_count": len(groups), "clusters": [{"cluster": key, "size": len(items), "matches": items} for key, items in sorted(groups.items())]}


def write_review(report: dict, output: Path) -> None:
    fields = ["cluster", "size", "candidate_branch", "evidence_limit", "review_notes"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for item in report["clusters"]:
            writer.writerow({"cluster": item["cluster"], "size": item["size"], "candidate_branch": "", "evidence_limit": "DNA inference requires lawful consent and documentary corroboration", "review_notes": ""})


def main() -> int:
    parser = argparse.ArgumentParser(description="Cluster DNA match rows by a declared key.")
    parser.add_argument("matches_csv")
    parser.add_argument("--key-col", default="cluster")
    parser.add_argument("--json-output", default="dna_clusters.json")
    parser.add_argument("--review-output", default="dna_cluster_review.csv")
    args = parser.parse_args()
    report = cluster(read(Path(args.matches_csv)), args.key_col)
    Path(args.json_output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_review(report, Path(args.review_output))
    print(json.dumps({"clusters": report["cluster_count"], "json": args.json_output, "review": args.review_output}, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
