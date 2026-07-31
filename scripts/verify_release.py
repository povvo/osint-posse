#!/usr/bin/env python3
"""Verify source-tree or distribution release gates without remote state."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 uses the declared compatibility dependency.
    import tomli as tomllib


VERSION = "0.1.0"
FORBIDDEN_PARTS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
    "osint_posse.egg-info",
}
SECRET_PATTERNS = {
    "OpenAI key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


class Verification:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def finish(self) -> int:
        for note in self.notes:
            print(f"PASS: {note}")
        for error in self.errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"release verification: {len(self.errors)} error(s)")
        return 1 if self.errors else 0


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def excluded(relative: Path) -> bool:
    if relative.name.endswith(":Zone.Identifier"):
        return True
    if any(part in FORBIDDEN_PARTS or part.endswith(".egg-info") for part in relative.parts):
        return True
    if relative.parts[:2] == ("docs", "research"):
        if relative.suffix.lower() == ".pdf":
            return True
        if len(relative.parts) > 2 and relative.parts[2] == "other" and relative.suffix == ".json":
            return True
    return False


def release_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not excluded(path.relative_to(root))
    )


def verify_source(root: Path) -> int:
    check = Verification()
    metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    version = metadata["project"]["version"]
    check.require(version == VERSION, f"pyproject version is {version!r}, expected {VERSION!r}")
    check.require("green-ink" in metadata["project"]["scripts"], "green-ink compatibility entry point is missing")
    lock = tomllib.loads((root / "uv.lock").read_text(encoding="utf-8"))
    locked_project = next(
        (package for package in lock.get("package", []) if package.get("name") == "osint-posse"),
        None,
    )
    check.require(locked_project is not None, "uv.lock omits the osint-posse project")
    if locked_project is not None:
        check.require(
            locked_project.get("version") == version,
            f"uv.lock project version is {locked_project.get('version')!r}, expected {version!r}",
        )

    skill = root / "src" / "skills" / "recon-rodeo"
    claude = root / "src" / ".claude" / "agents"
    codex = root / "src" / ".codex" / "agents"
    check.require((skill / "SKILL.md").is_file(), "Recon Rodeo SKILL.md is missing")
    check.require(len(list(claude.glob("*.md"))) == 60, "source tree must contain exactly 60 Claude agents")
    check.require(len(list(codex.glob("*.toml"))) == 60, "source tree must contain exactly 60 Codex agents")

    files = release_files(root)
    for path in files:
        relative = path.relative_to(root)
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
            except (SyntaxError, UnicodeDecodeError) as exc:
                check.errors.append(f"invalid Python {relative}: {exc}")
        elif path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                check.errors.append(f"invalid JSON {relative}: {exc}")
        elif path.suffix == ".toml":
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
                check.errors.append(f"invalid TOML {relative}: {exc}")

        if path.stat().st_size <= 2_000_000:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    check.errors.append(f"possible {label} in {relative}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    for claim in ("pip install osint-posse\n", "[1.0.0]", "actions/workflows/ci.yml/badge"):
        check.require(claim not in readme + changelog, f"unreleased public-state claim remains: {claim!r}")
    for link in re.findall(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)", readme):
        check.require((root / link).exists(), f"README relative link is missing: {link}")

    ledger_path = root / "docs" / "research" / "provenance.csv"
    check.require(ledger_path.is_file(), "research provenance ledger is missing")
    if ledger_path.is_file():
        with ledger_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        required = {
            "path",
            "source_url",
            "author",
            "licence",
            "retrieved_at",
            "sha256",
            "purpose",
            "redistribute",
            "decision_owner",
            "decision_date",
        }
        check.require(required.issubset(rows[0].keys() if rows else (csv.DictReader(
            ledger_path.read_text(encoding="utf-8").splitlines()
        ).fieldnames or [])), "provenance ledger headers are incomplete")
        for row in rows:
            if row.get("redistribute", "").strip().lower() == "yes":
                missing = sorted(column for column in required if not row.get(column, "").strip())
                check.require(not missing, f"admitted research row is incomplete: {row.get('path')}: {missing}")
                artifact = root / row["path"]
                check.require(artifact.is_file(), f"admitted research artefact is missing: {row['path']}")
                if artifact.is_file():
                    check.require(sha256(artifact) == row["sha256"], f"research hash mismatch: {row['path']}")

    path_inventory_digest = hashlib.sha256(
        "\n".join(str(path.relative_to(root)) for path in files).encode("utf-8")
    ).hexdigest()
    check.notes.extend(
        [
            f"source path inventory contains {len(files)} release-eligible files",
            f"source path-inventory sha256 {path_inventory_digest}",
            "60 Claude and 60 Codex agent definitions are present",
        ]
    )
    return check.finish()


def archive_members(path: Path) -> list[str]:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            return archive.namelist()
    with tarfile.open(path, "r:*") as archive:
        return archive.getnames()


def verify_dist(directory: Path) -> int:
    check = Verification()
    archives = sorted(
        path for path in directory.iterdir() if path.is_file() and (path.suffix == ".whl" or path.name.endswith(".tar.gz"))
    )
    check.require(bool(archives), f"no wheel or sdist found in {directory}")
    for archive in archives:
        members = archive_members(archive)
        wheel = archive.suffix == ".whl"
        check.require(VERSION in archive.name, f"artefact filename version mismatch: {archive.name}")
        check.require(
            not any(
                member.endswith(":Zone.Identifier")
                or "__pycache__" in PurePosixPath(member).parts
                or member.endswith(".pyc")
                or (
                    "/docs/research/" in f"/{member}"
                    and (member.endswith(".pdf") or member.endswith(".json"))
                )
                for member in members
            ),
            f"artefact contains quarantined or generated paths: {archive.name}",
        )
        if wheel:
            claude_count = sum(
                member.startswith("ospo/data/agents/claude/") and member.endswith(".md")
                for member in members
            )
            codex_count = sum(
                member.startswith("ospo/data/agents/codex/") and member.endswith(".toml")
                for member in members
            )
            check.require("ospo/data/recon-rodeo/SKILL.md" in members, "wheel omits Recon Rodeo")
            check.require(claude_count == 60, f"wheel has {claude_count} Claude agents, expected 60")
            check.require(codex_count == 60, f"wheel has {codex_count} Codex agents, expected 60")
        else:
            for public_path in (
                "docs/evidence-and-provenance.md",
                "docs/privacy-and-data-handling.md",
                "docs/release-process.md",
                "docs/responsible-use.md",
                "docs/security-model.md",
                "docs/research/README.md",
                "docs/research/provenance.csv",
            ):
                check.require(
                    any(member.endswith(f"/{public_path}") for member in members),
                    f"sdist omits public release document: {public_path}",
                )
            check.require(
                any(member.endswith("/src/skills/recon-rodeo/SKILL.md") for member in members),
                "sdist omits canonical Recon Rodeo source",
            )
            check.require(
                sum("/src/.claude/agents/" in member and member.endswith(".md") for member in members) == 60,
                "sdist does not contain exactly 60 Claude agents",
            )
            check.require(
                sum("/src/.codex/agents/" in member and member.endswith(".toml") for member in members) == 60,
                "sdist does not contain exactly 60 Codex agents",
            )
        check.notes.append(f"{archive.name}: {len(members)} members, sha256 {sha256(archive)}")
    return check.finish()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source", type=Path)
    mode.add_argument("--dist", type=Path)
    arguments = parser.parse_args()
    if arguments.source is not None:
        return verify_source(arguments.source.resolve())
    return verify_dist(arguments.dist.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
