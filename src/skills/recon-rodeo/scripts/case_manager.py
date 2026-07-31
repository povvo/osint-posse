#!/usr/bin/env python3
"""
ospo :: case manager

Creates repeatable local case folders, evidence indexes, audit logs, and
verifiable ZIP export packages.

Security properties:
- Case inputs must resolve beneath the configured case root.
- Filesystem links, Windows junctions, and reparse points are refused.
- ZIP exports exclude cache and prior exports by default.
- Export creation uses a temporary file followed by atomic replacement.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import tempfile
import zipfile
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from osint_common import JsonlAuditLog, ensure_dir, sha256_file, slugify, utc_now, write_json

JsonDict = dict[str, Any]

CASE_MANIFEST_NAME = "case_manifest.json"
EVIDENCE_INDEX_NAME = "evidence_index.json"
AUDIT_LOG_RELATIVE_PATH = Path("logs") / "audit.jsonl"
EXPORT_EXCLUDED_TOP_LEVEL = frozenset({"cache", "exports"})
SUBDIRS = (
    "raw",
    "processed",
    "evidence",
    "reports",
    "graphs",
    "logs",
    "exports",
    "cache",
)


def _is_link_or_reparse(path: Path) -> bool:
    """Return whether a path is a symlink, Windows junction, or reparse point."""
    stat_result = path.lstat()
    attributes = getattr(stat_result, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(stat_result.st_mode) or bool(attributes & reparse_flag)


def _resolve_contained(root: Path, candidate: Path, *, strict: bool = True) -> Path:
    """Resolve candidate and ensure that it stays below root."""
    resolved_root = root.resolve(strict=True)
    resolved_candidate = candidate.resolve(strict=strict)

    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"Path escapes configured case root: {candidate}") from exc

    return resolved_candidate


def _safe_files(root: Path) -> Iterator[Path]:
    """Yield regular files recursively while refusing all link-like entries.

    This protects ordinary local filesystem traversal. It cannot make a hostile,
    concurrently modified filesystem fully race-free; run case workspaces with
    appropriate OS-level access controls.
    """
    resolved_root = root.resolve(strict=True)
    if not resolved_root.is_dir():
        raise NotADirectoryError(f"Expected directory: {root}")
    if _is_link_or_reparse(resolved_root):
        raise ValueError(f"Refusing link or reparse-point root: {root}")

    pending = [resolved_root]

    while pending:
        directory = pending.pop()

        with os.scandir(directory) as entries:
            for entry in entries:
                item = Path(entry.path)

                if _is_link_or_reparse(item):
                    raise ValueError(
                        f"Case traversal refuses links and reparse points: {item}"
                    )

                resolved_item = _resolve_contained(resolved_root, item)

                if entry.is_dir(follow_symlinks=False):
                    pending.append(resolved_item)
                elif entry.is_file(follow_symlinks=False):
                    yield resolved_item


@dataclass(frozen=True)
class CaseManifest:
    """Metadata persisted at the root of a case workspace."""

    case_id: str
    title: str
    created_at_utc: str = field(default_factory=utc_now)
    analyst: str = "ospo"
    description: str = ""
    handling_notes: str = (
        "Public-source OSINT case. Validate all leads before analytical judgement."
    )
    directories: dict[str, str] = field(default_factory=dict)


class CaseManager:
    """Filesystem-backed, locally contained case workspace manager."""

    def __init__(self, root_dir: str | Path = "./cases") -> None:
        self.root_dir = Path(ensure_dir(root_dir)).resolve(strict=True)

    def _case_path(self, case_id_or_path: str | Path) -> Path:
        """Resolve a case ID/path and ensure it belongs to this manager's root."""
        supplied = Path(case_id_or_path)

        candidate = (
            supplied
            if supplied.is_absolute()
            else self.root_dir / supplied
        )
        resolved = _resolve_contained(self.root_dir, candidate)

        if _is_link_or_reparse(resolved):
            raise ValueError(f"Case directory must not be a link or reparse point: {resolved}")
        if not resolved.is_dir():
            raise NotADirectoryError(f"Case path is not a directory: {resolved}")

        manifest_path = resolved / CASE_MANIFEST_NAME
        if not manifest_path.is_file():
            raise FileNotFoundError(f"No {CASE_MANIFEST_NAME} under {resolved}")

        return resolved

    @staticmethod
    def _audit_log(case_dir: Path) -> JsonlAuditLog:
        """Return the audit logger for an already validated case directory."""
        return JsonlAuditLog(case_dir / AUDIT_LOG_RELATIVE_PATH)

    def create_case(
        self,
        title: str,
        analyst: str = "ospo",
        description: str = "",
    ) -> JsonDict:
        """Create a new case workspace without overwriting an existing one."""
        normalized_title = title.strip()
        normalized_analyst = analyst.strip()

        if not normalized_title:
            raise ValueError("title must not be empty")
        if not normalized_analyst:
            raise ValueError("analyst must not be empty")

        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        case_id = f"{timestamp}_{slugify(normalized_title, 50)}"
        case_dir = self.root_dir / case_id

        try:
            case_dir.mkdir(mode=0o750)
        except FileExistsError as exc:
            raise FileExistsError(
                f"Case ID collision: {case_id}. Retry creation to obtain a new timestamp."
            ) from exc

        try:
            directories = {
                name: str((case_dir / name).resolve())
                for name in SUBDIRS
            }
            for directory in directories.values():
                Path(directory).mkdir(mode=0o750)

            manifest = CaseManifest(
                case_id=case_id,
                title=normalized_title,
                analyst=normalized_analyst,
                description=description,
                directories=directories,
            )
            write_json(case_dir / CASE_MANIFEST_NAME, asdict(manifest))
            self._audit_log(case_dir).write(
                "case_created",
                case_id=case_id,
                title=normalized_title,
                analyst=normalized_analyst,
            )
        except Exception:
            # The workspace contains no user-supplied evidence at this stage.
            # Remove an incomplete case rather than leaving a valid-looking one.
            for item in sorted(case_dir.rglob("*"), reverse=True):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    item.rmdir()
            case_dir.rmdir()
            raise

        return {
            "case_id": case_id,
            "case_dir": str(case_dir),
            "manifest": asdict(manifest),
        }

    def load_case(self, case_id_or_path: str | Path) -> JsonDict:
        """Load and minimally validate a case manifest."""
        case_dir = self._case_path(case_id_or_path)
        manifest_path = case_dir / CASE_MANIFEST_NAME

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in manifest: {manifest_path}") from exc

        if not isinstance(manifest, dict):
            raise ValueError(f"Manifest must be a JSON object: {manifest_path}")
        if manifest.get("case_id") != case_dir.name:
            raise ValueError(
                f"Manifest case_id does not match directory name: {case_dir}"
            )

        return manifest

    def index_evidence(self, case_id_or_path: str | Path) -> JsonDict:
        """Generate a SHA-256 evidence index for regular evidence files."""
        case_dir = self._case_path(case_id_or_path)
        evidence_root = case_dir / "evidence"

        if not evidence_root.is_dir():
            raise FileNotFoundError(f"Evidence directory does not exist: {evidence_root}")

        rows: list[JsonDict] = []
        for item in sorted(_safe_files(evidence_root), key=lambda path: path.as_posix()):
            item_stat = item.stat()
            rows.append(
                {
                    "path": item.relative_to(case_dir).as_posix(),
                    "bytes": item_stat.st_size,
                    "sha256": sha256_file(item),
                    "modified_utc": datetime.fromtimestamp(
                        item_stat.st_mtime,
                        UTC,
                    ).isoformat(),
                }
            )

        index: JsonDict = {
            "case_id": case_dir.name,
            "generated_at_utc": utc_now(),
            "algorithm": "sha256",
            "evidence_files": rows,
            "total_files": len(rows),
            "total_bytes": sum(row["bytes"] for row in rows),
        }

        write_json(case_dir / EVIDENCE_INDEX_NAME, index)
        self._audit_log(case_dir).write(
            "evidence_indexed",
            total_files=index["total_files"],
            total_bytes=index["total_bytes"],
        )
        return index

    def add_note(
        self,
        case_id_or_path: str | Path,
        note: str,
        note_type: str = "analyst_note",
    ) -> JsonDict:
        """Append a non-empty analyst note to the append-only audit log."""
        case_dir = self._case_path(case_id_or_path)

        if not note.strip():
            raise ValueError("note must not be empty")
        if not note_type.replace("_", "").isalnum():
            raise ValueError("note_type must contain only letters, numbers, and underscores")

        return self._audit_log(case_dir).write(note_type, note=note)

    def _export_files(self, case_dir: Path) -> list[Path]:
        """Return eligible package files, excluding volatile/internal directories."""
        files: list[Path] = []

        for item in _safe_files(case_dir):
            relative = item.relative_to(case_dir)
            if relative.parts and relative.parts[0] in EXPORT_EXCLUDED_TOP_LEVEL:
                continue
            files.append(item)

        return sorted(files, key=lambda path: path.relative_to(case_dir).as_posix())

    def _resolve_output_path(
        self,
        case_dir: Path,
        output_path: str | Path | None,
    ) -> Path:
        """Resolve output path and ensure an explicit path cannot escape case root."""
        if output_path is None:
            output = case_dir / "exports" / f"{case_dir.name}.zip"
        else:
            supplied = Path(output_path)
            output = supplied if supplied.is_absolute() else Path.cwd() / supplied
            output = output.resolve(strict=False)

        if output.suffix.lower() != ".zip":
            raise ValueError("Export output path must have a .zip suffix")
        if output.exists():
            raise FileExistsError(f"Refusing to overwrite existing export: {output}")

        return output

    def export_case(
        self,
        case_id_or_path: str | Path,
        output_path: str | Path | None = None,
    ) -> JsonDict:
        """Build a ZIP package and a sidecar manifest without overwriting files."""
        case_dir = self._case_path(case_id_or_path)
        evidence_index = self.index_evidence(case_dir)

        output = self._resolve_output_path(case_dir, output_path)
        output.parent.mkdir(parents=True, exist_ok=True, mode=0o750)

        self._audit_log(case_dir).write(
            "case_export_started",
            output=str(output),
            evidence_index_sha256=sha256_file(case_dir / EVIDENCE_INDEX_NAME),
        )

        source_files = self._export_files(case_dir)
        archive_entries: list[JsonDict] = []

        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{case_dir.name}_",
            suffix=".zip.tmp",
            dir=output.parent,
        )
        os.close(descriptor)
        temporary_output = Path(temporary_name)

        try:
            with zipfile.ZipFile(
                temporary_output,
                mode="x",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,
                strict_timestamps=False,
            ) as archive:
                for item in source_files:
                    relative = item.relative_to(case_dir)
                    archive_name = (Path(case_dir.name) / relative).as_posix()
                    item_stat = item.stat()

                    archive.write(item, archive_name)
                    archive_entries.append(
                        {
                            "path": relative.as_posix(),
                            "archive_path": archive_name,
                            "bytes": item_stat.st_size,
                            "sha256": sha256_file(item),
                        }
                    )

                package_manifest: JsonDict = {
                    "case_id": case_dir.name,
                    "created_at_utc": utc_now(),
                    "archive_format": "zip",
                    "hash_algorithm": "sha256",
                    "evidence_index_sha256": sha256_file(
                        case_dir / EVIDENCE_INDEX_NAME
                    ),
                    "evidence_file_count": evidence_index["total_files"],
                    "included_files": archive_entries,
                    "excluded_top_level_directories": sorted(EXPORT_EXCLUDED_TOP_LEVEL),
                }
                archive.writestr(
                    f"{case_dir.name}/package_manifest.json",
                    json.dumps(package_manifest, indent=2, sort_keys=True) + "\n",
                )

            os.replace(temporary_output, output)
        except Exception:
            temporary_output.unlink(missing_ok=True)
            raise

        export_sha256 = sha256_file(output)
        sidecar_path = output.with_suffix(f"{output.suffix}.manifest.json")
        sidecar: JsonDict = {
            "case_id": case_dir.name,
            "export_path": str(output),
            "export_sha256": export_sha256,
            "created_at_utc": utc_now(),
            "included_file_count": len(archive_entries),
        }
        write_json(sidecar_path, sidecar)

        self._audit_log(case_dir).write(
            "case_exported",
            output=str(output),
            sha256=export_sha256,
            sidecar_manifest=str(sidecar_path),
            included_file_count=len(archive_entries),
        )

        return {
            "output_path": str(output),
            "sha256": export_sha256,
            "sidecar_manifest_path": str(sidecar_path),
            "included_file_count": len(archive_entries),
        }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create and manage local OSINT case folders"
    )
    parser.add_argument("--root", default="./cases", help="Case workspace root")

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new case")
    create_parser.add_argument("title")
    create_parser.add_argument("--analyst", default="ospo")
    create_parser.add_argument("--description", default="")

    index_parser = subparsers.add_parser("index", help="Create an evidence hash index")
    index_parser.add_argument("case")

    note_parser = subparsers.add_parser("note", help="Append an analyst note")
    note_parser.add_argument("case")
    note_parser.add_argument("note")
    note_parser.add_argument("--type", default="analyst_note", dest="note_type")

    export_parser = subparsers.add_parser("export", help="Build a ZIP case package")
    export_parser.add_argument("case")
    export_parser.add_argument("--out", default=None)

    args = parser.parse_args()
    manager = CaseManager(args.root)

    if args.command == "create":
        result = manager.create_case(args.title, args.analyst, args.description)
    elif args.command == "index":
        result = manager.index_evidence(args.case)
    elif args.command == "note":
        result = manager.add_note(args.case, args.note, args.note_type)
    elif args.command == "export":
        result = manager.export_case(args.case, args.out)
    else:
        parser.error(f"Unsupported command: {args.command}")
        return

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()