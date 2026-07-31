"""Ownership-safe installation and removal of bundled release resources."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from ._paths import InstallPaths, install_paths, release_resources

SCHEMA_VERSION = "1.0"


class InstallConflict(RuntimeError):
    """Raised when an operation would overwrite a file ospo cannot prove it owns."""


@dataclass
class OperationResult:
    action: str
    dry_run: bool
    copied: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    preserved: list[str] = field(default_factory=list)


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _load_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallConflict(f"Ownership record is unreadable: {path}: {exc}") from exc
    if payload.get("schema_version") != SCHEMA_VERSION or not isinstance(payload.get("files"), dict):
        raise InstallConflict(f"Ownership record has an unsupported schema: {path}")
    files = payload["files"]
    if any(not isinstance(key, str) or not isinstance(value, str) for key, value in files.items()):
        raise InstallConflict(f"Ownership record contains invalid file entries: {path}")
    return dict(files)


def _assert_within_root(root: Path, path: Path) -> None:
    """Reject destinations whose existing symlink ancestry escapes the scope root."""
    resolved_root = root.resolve()
    try:
        path.resolve(strict=False).relative_to(resolved_root)
    except ValueError as exc:
        raise InstallConflict(f"Destination escapes the selected scope root: {path}") from exc


def _write_manifest(path: Path, files: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": SCHEMA_VERSION, "files": dict(sorted(files.items()))}
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _ownership_key(root: Path, destination: Path) -> str:
    return destination.relative_to(root).as_posix()


def _owned_destination(root: Path, key: str) -> Path:
    if Path(key).is_absolute():
        raise InstallConflict(
            "Ownership record contains an obsolete absolute path; "
            "reinstall before moving the project"
        )
    destination = root / Path(key)
    _assert_within_root(root, destination)
    return destination


def _atomic_copy(source: Path, destination: Path) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copy2(source, temporary)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _selected_sources(
    paths: InstallPaths,
    *,
    skill: bool,
    claude: bool,
    codex: bool,
) -> list[tuple[Path, Path]]:
    resources = release_resources()
    selected: list[tuple[Path, Path]] = []
    if skill:
        selected.append((resources.skill, paths.skill))
    if claude:
        selected.append((resources.claude_agents, paths.claude_agents))
    if codex:
        selected.append((resources.codex_agents, paths.codex_agents))
    return selected


def _file_plan(mappings: list[tuple[Path, Path]]) -> list[tuple[Path, Path]]:
    plan: list[tuple[Path, Path]] = []
    for source_root, destination_root in mappings:
        if not source_root.is_dir():
            raise InstallConflict(f"Release resource directory is missing: {source_root}")
        for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
            if source.name.endswith(":Zone.Identifier") or "__pycache__" in source.parts:
                continue
            plan.append((source, destination_root / source.relative_to(source_root)))
    return plan


def install_release(
    *,
    scope: str = "project",
    root: Path | None = None,
    skill: bool = True,
    claude: bool = False,
    codex: bool = False,
    dry_run: bool = False,
) -> OperationResult:
    """Install selected resources after a complete collision preflight."""
    paths = install_paths(scope, root)
    _assert_within_root(paths.root, paths.ownership)
    ownership = _load_manifest(paths.ownership)
    plan = _file_plan(
        _selected_sources(paths, skill=skill, claude=claude, codex=codex)
    )
    result = OperationResult(action="install", dry_run=dry_run)

    for source, destination in plan:
        _assert_within_root(paths.root, destination)
        source_hash = _digest(source)
        key = _ownership_key(paths.root, destination)
        display = str(destination)
        if not destination.exists():
            result.copied.append(display)
            continue
        if not destination.is_file() or destination.is_symlink():
            raise InstallConflict(f"Destination is not a regular file: {destination}")
        current_hash = _digest(destination)
        recorded_hash = ownership.get(key)
        if current_hash == source_hash:
            result.unchanged.append(display)
            continue
        if recorded_hash is None:
            raise InstallConflict(f"Refusing to overwrite an unowned file: {destination}")
        if current_hash != recorded_hash:
            raise InstallConflict(f"Refusing to overwrite a modified installed file: {destination}")
        result.copied.append(display)

    if dry_run:
        return result

    for source, destination in plan:
        source_hash = _digest(source)
        key = _ownership_key(paths.root, destination)
        display = str(destination)
        if display in result.copied:
            destination.parent.mkdir(parents=True, exist_ok=True)
            _atomic_copy(source, destination)
            ownership[key] = source_hash
            _write_manifest(paths.ownership, ownership)
        elif display in result.unchanged and key in ownership:
            ownership[key] = source_hash
    _write_manifest(paths.ownership, ownership)
    return result


def uninstall_release(
    *,
    scope: str = "project",
    root: Path | None = None,
    skill: bool = True,
    claude: bool = False,
    codex: bool = False,
    dry_run: bool = False,
) -> OperationResult:
    """Remove only unchanged files recorded as owned by ospo."""
    paths = install_paths(scope, root)
    _assert_within_root(paths.root, paths.ownership)
    ownership = _load_manifest(paths.ownership)
    plan = _file_plan(
        _selected_sources(paths, skill=skill, claude=claude, codex=codex)
    )
    source_roots = [
        destination
        for _source, destination in _selected_sources(
            paths, skill=skill, claude=claude, codex=codex
        )
    ]
    root_keys = [_ownership_key(paths.root, destination) for destination in source_roots]
    selected = {_ownership_key(paths.root, destination) for _source, destination in plan}
    selected.update(
        key
        for key in ownership
        if any(key == root_key or key.startswith(f"{root_key}/") for root_key in root_keys)
    )
    result = OperationResult(action="uninstall", dry_run=dry_run)
    removed_keys: list[str] = []
    preserved_keys: list[str] = []

    for key in sorted(selected):
        recorded_hash = ownership.get(key)
        if recorded_hash is None:
            continue
        destination = _owned_destination(paths.root, key)
        if not destination.exists():
            removed_keys.append(key)
            result.removed.append(str(destination))
        elif destination.is_file() and not destination.is_symlink() and _digest(destination) == recorded_hash:
            removed_keys.append(key)
            result.removed.append(str(destination))
        else:
            preserved_keys.append(key)
            result.preserved.append(str(destination))

    if dry_run:
        return result

    for key in removed_keys:
        destination = _owned_destination(paths.root, key)
        if destination.exists():
            destination.unlink()
        ownership.pop(key, None)
    for key in preserved_keys:
        ownership.pop(key, None)

    for root_path in source_roots:
        if root_path.is_dir():
            for directory in sorted(
                (path for path in root_path.rglob("*") if path.is_dir()),
                key=lambda path: len(path.parts),
                reverse=True,
            ):
                try:
                    directory.rmdir()
                except OSError:
                    pass
            try:
                root_path.rmdir()
            except OSError:
                pass

    if ownership:
        _write_manifest(paths.ownership, ownership)
    elif paths.ownership.exists():
        paths.ownership.unlink()
    return result
