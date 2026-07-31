"""PEP 517 backend for bundling canonical OSINT Posse resources."""

from __future__ import annotations

import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

from setuptools import build_meta as _setuptools_backend
from setuptools.command.build_py import build_py

ROOT = Path(__file__).resolve().parents[2]
SDIST_FILES = (
    Path("CHANGELOG.md"),
    Path("resources/README.md"),
    Path("resources/build/ospo_build_backend.py"),
)
SDIST_TREES = (
    (Path("resources/docs"), {".csv", ".md"}),
    (Path("src/.claude/agents"), {".md"}),
    (Path("src/.codex/agents"), {".toml"}),
    (Path("src/skills/recon-rodeo"), None),
)


def _release_resource_files() -> list[str]:
    """Return the non-package files deliberately admitted to the sdist."""

    files = [ROOT / relative for relative in SDIST_FILES]
    for relative, suffixes in SDIST_TREES:
        for path in (ROOT / relative).rglob("*"):
            if not path.is_file():
                continue
            if suffixes is not None and path.suffix not in suffixes:
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            if path.match("test_*.py") or path.match("*_test.py"):
                continue
            if path.name.endswith(":Zone.Identifier"):
                continue
            files.append(path)
    missing = [path for path in files if not path.is_file()]
    if missing:
        raise RuntimeError(f"Required release resource is missing: {missing[0]}")
    return sorted(path.relative_to(ROOT).as_posix() for path in files)


class BuildWithResources(build_py):
    """Copy source-controlled skill and agent resources into ``ospo.data``."""

    def run(self) -> None:
        super().run()
        package_data = Path(self.build_lib) / "ospo" / "data"
        mappings = (
            (ROOT / "src" / "skills" / "recon-rodeo", package_data / "recon-rodeo"),
            (ROOT / "src" / ".claude" / "agents", package_data / "agents" / "claude"),
            (ROOT / "src" / ".codex" / "agents", package_data / "agents" / "codex"),
        )
        for source, destination in mappings:
            if not source.is_dir():
                raise RuntimeError(f"Required release resource directory is missing: {source}")
            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    "__pycache__",
                    "*.pyc",
                    "test_*.py",
                    "*_test.py",
                    "*:Zone.Identifier",
                ),
            )


def build_sdist(
    sdist_directory: str,
    config_settings: dict[str, object] | None = None,
) -> str:
    """Build and complete the sdist from the backend-owned inventory."""

    filename = _setuptools_backend.build_sdist(sdist_directory, config_settings)
    archive = Path(sdist_directory) / filename
    with tempfile.TemporaryDirectory(prefix="ospo-sdist-") as temporary_directory:
        staging = Path(temporary_directory)
        with tarfile.open(archive, "r:gz") as source:
            members = source.getmembers()
            roots = {PurePosixPath(member.name).parts[0] for member in members}
            if len(roots) != 1:
                raise RuntimeError("Generated sdist does not have one release root")
            for member in members:
                destination = (staging / member.name).resolve()
                if staging.resolve() not in destination.parents:
                    raise RuntimeError(f"Unsafe generated sdist member: {member.name}")
                if member.issym() or member.islnk():
                    raise RuntimeError(f"Linked generated sdist member: {member.name}")
            source.extractall(staging)

        release_root = staging / roots.pop()
        resources = _release_resource_files()
        for relative in resources:
            destination = release_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

        source_manifests = list((release_root / "src").glob("*.egg-info/SOURCES.txt"))
        if len(source_manifests) != 1:
            raise RuntimeError("Generated sdist does not have one source manifest")
        source_manifest = source_manifests[0]
        entries = set(source_manifest.read_text(encoding="utf-8").splitlines())
        entries.update(resources)
        source_manifest.write_text(
            "\n".join(sorted(entries)) + "\n",
            encoding="utf-8",
        )

        with tempfile.NamedTemporaryFile(
            dir=archive.parent,
            prefix=f".{archive.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_archive:
            rebuilt = Path(temporary_archive.name)
        try:
            with tarfile.open(rebuilt, "w:gz") as destination:
                destination.add(release_root, arcname=release_root.name)
            rebuilt.replace(archive)
        finally:
            rebuilt.unlink(missing_ok=True)
    return filename


build_wheel = _setuptools_backend.build_wheel
build_editable = _setuptools_backend.build_editable
get_requires_for_build_sdist = _setuptools_backend.get_requires_for_build_sdist
get_requires_for_build_wheel = _setuptools_backend.get_requires_for_build_wheel
get_requires_for_build_editable = _setuptools_backend.get_requires_for_build_editable
prepare_metadata_for_build_wheel = _setuptools_backend.prepare_metadata_for_build_wheel
prepare_metadata_for_build_editable = _setuptools_backend.prepare_metadata_for_build_editable
