#!/usr/bin/env python3
"""Universal Metadata Tagging.

Applies a consistent metadata envelope to local files or tabular records. Produces
sidecar JSON files and a consolidated tag index.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

CORE_FIELDS = ["case_id", "source_ref", "handling", "confidence", "tags", "notes"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sidecar_for(path: Path, case_id: str, source_ref: str, tags: list[str], handling: str, confidence: str, notes: str) -> dict:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(path)
    return {"path": str(path), "file_name": path.name, "bytes": path.stat().st_size, "sha256": sha256(path), "case_id": case_id, "source_ref": source_ref, "handling": handling, "confidence": confidence, "tags": tags, "notes": notes, "tagged_at_utc": now()}


def tag_files(files: list[str], output_dir: Path, args: argparse.Namespace) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for item in files:
        path = Path(item)
        record = sidecar_for(path, args.case_id, args.source_ref, args.tag or [], args.handling, args.confidence, args.notes or "")
        sidecar = output_dir / f"{path.name}.metadata.json"
        sidecar.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        record["sidecar"] = str(sidecar)
        records.append(record)
    index_path = output_dir / "metadata_index.json"
    index_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"records": len(records), "index": str(index_path), "items": records}


def tag_csv(input_csv: Path, output_csv: Path, args: argparse.Namespace) -> dict:
    with input_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []
    for field in CORE_FIELDS:
        if field not in fieldnames: fieldnames.append(field)
    for row in rows:
        row.update({"case_id": args.case_id, "source_ref": args.source_ref, "handling": args.handling, "confidence": args.confidence, "tags": ";".join(args.tag or []), "notes": args.notes or ""})
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    return {"input": str(input_csv), "output": str(output_csv), "rows": len(rows), "fields": fieldnames}


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply standard metadata tags to files or CSV rows.")
    ap.add_argument("--case-id", required=True); ap.add_argument("--source-ref", default="")
    ap.add_argument("--handling", default="standard"); ap.add_argument("--confidence", choices=["low", "medium", "high"], default="low")
    ap.add_argument("--tag", action="append"); ap.add_argument("--notes")
    ap.add_argument("--file", action="append", default=[]); ap.add_argument("--output-dir", default="metadata_sidecars")
    ap.add_argument("--csv"); ap.add_argument("--csv-output")
    args = ap.parse_args()
    if args.csv:
        if not args.csv_output: ap.error("--csv-output is required with --csv")
        print(json.dumps(tag_csv(Path(args.csv), Path(args.csv_output), args), indent=2)); return 0
    if not args.file: ap.error("at least one --file or --csv is required")
    print(json.dumps(tag_files(args.file, Path(args.output_dir), args), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
