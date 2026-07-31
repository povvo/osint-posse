#!/usr/bin/env python3
"""Resource Allocation and Tasking.

Assigns tasks to available resources by capacity, priority, and required skill.
Writes an allocation table and highlights unassigned work.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def score_priority(value: str) -> int:
    return {"critical": 0, "high": 1, "normal": 2, "low": 3}.get(value.lower(), 2)


def allocate(tasks: list[dict], people: list[dict]) -> dict:
    capacity = {p.get("name", ""): int(p.get("capacity", 0) or 0) for p in people if p.get("name")}
    skills = {p.get("name", ""): {s.strip().lower() for s in p.get("skills", "").split(";") if s.strip()} for p in people if p.get("name")}
    assigned, unassigned = [], []
    for task in sorted(tasks, key=lambda r: score_priority(r.get("priority", "normal"))):
        required = {s.strip().lower() for s in task.get("required_skills", "").split(";") if s.strip()}
        candidates = [name for name in capacity if capacity[name] > 0 and required.issubset(skills.get(name, set()))]
        if not candidates:
            unassigned.append(task); continue
        chosen = sorted(candidates, key=lambda n: (-capacity[n], n))[0]
        capacity[chosen] -= 1
        assigned.append({**task, "assigned_to": chosen})
    return {"assigned": assigned, "unassigned": unassigned, "remaining_capacity": capacity}


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = sorted({k for row in rows for k in row}) if rows else ["status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Allocate tasks to resources by skill and capacity.")
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--resources", required=True)
    ap.add_argument("--output-dir", default="allocation")
    args = ap.parse_args()
    result = allocate(read_csv(Path(args.tasks)), read_csv(Path(args.resources)))
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "assigned.csv", result["assigned"]); write_csv(out / "unassigned.csv", result["unassigned"])
    (out / "allocation_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"assigned": len(result["assigned"]), "unassigned": len(result["unassigned"]), "output_dir": str(out)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
