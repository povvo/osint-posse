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
    ".ruff_cache",
    ".wrangler",
    "venv",
    "build",
    "dist",
    "node_modules",
    "osint_posse.egg-info",
}
SECRET_PATTERNS = {
    "OpenAI key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "PyPI token": re.compile(r"\bpypi-[A-Za-z0-9_-]{50,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
MCP_PACKAGES = (
    Path("src/tools/recommended/mcp/ospo-reframe"),
    Path("src/tools/recommended/mcp/ospo-pigeon-profile"),
    Path("src/database/ospo-db"),
)


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
    if relative.parts[:2] == ("resources", "dev"):
        return True
    if relative.parts[:3] == ("resources", "docs", "research"):
        if relative.suffix.lower() == ".pdf":
            return True
        if len(relative.parts) > 3 and relative.parts[3] == "other" and relative.suffix == ".json":
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
    check.require("green-ink" in metadata["project"]["scripts"], "Green Ink controller CLI entry point is missing")
    check.require(
        metadata["project"].get("urls", {}).get("Repository") == "https://github.com/povvo/osint-posse",
        "pyproject repository URL is missing or incorrect",
    )
    check.require(
        {"name": "Ethan", "email": "povvo.dev@gmail.com"} in metadata["project"].get("authors", []),
        "pyproject author identity is missing or incorrect",
    )
    check.require(
        metadata.get("build-system", {}).get("build-backend") == "ospo_build_backend",
        "source-distribution inventory is not owned by the in-tree build backend",
    )
    for unwanted_root_file in ("MANIFEST.in", "setup.py", "uv.lock"):
        check.require(
            not (root / unwanted_root_file).exists(),
            f"unwanted root build artefact is present: {unwanted_root_file}",
        )
    requirements_path = root / "resources" / "dev" / "requirements.txt"
    requirements = {
        line.strip().replace('"', "'")
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    project_requirements = {
        requirement.replace('"', "'")
        for requirement in metadata["project"].get("dependencies", [])
    }
    check.require(
        requirements == project_requirements,
        "resources/dev/requirements.txt does not exactly mirror pyproject core dependencies",
    )

    required_mcp_dependencies = {
        "agents": "^0.20.1",
        "@modelcontextprotocol/sdk": "^1.30.0",
        "zod": "^4.0.0",
    }
    for relative in MCP_PACKAGES:
        package_path = root / relative / "package.json"
        lock_path = root / relative / "package-lock.json"
        check.require(package_path.is_file(), f"MCP package metadata is missing: {relative}")
        check.require(lock_path.is_file(), f"MCP dependency lockfile is missing: {relative}")
        if not package_path.is_file() or not lock_path.is_file():
            continue
        package = json.loads(package_path.read_text(encoding="utf-8"))
        package_lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock_root = package_lock.get("packages", {}).get("", {})
        dependencies = package.get("dependencies", {})
        check.require(package.get("private") is True, f"MCP package must remain private: {relative}")
        check.require(package.get("version") == VERSION, f"MCP package version mismatch: {relative}")
        check.require(
            package_lock.get("lockfileVersion", 0) >= 3,
            f"MCP package requires an npm v3 lockfile: {relative}",
        )
        check.require(lock_root.get("name") == package.get("name"), f"MCP lockfile name mismatch: {relative}")
        check.require(lock_root.get("version") == package.get("version"), f"MCP lockfile version mismatch: {relative}")
        package_requirements = (
            {} if relative.name == "ospo-db" else required_mcp_dependencies
        )
        for dependency, requirement in package_requirements.items():
            check.require(
                dependencies.get(dependency) == requirement,
                f"MCP dependency {dependency!r} is not pinned to {requirement!r}: {relative}",
            )
            check.require(
                lock_root.get("dependencies", {}).get(dependency) == requirement,
                f"MCP lockfile dependency {dependency!r} does not match package.json: {relative}",
            )
        check.require(
            package.get("scripts", {}).get("typecheck")
            == ("node --check worker.js" if relative.name == "ospo-db" else "tsc --noEmit"),
            f"MCP package type-check script is missing: {relative}",
        )
        check.require(
            package.get("scripts", {}).get("build")
            == (
                "node --check worker.js"
                if relative.name == "ospo-db"
                else "wrangler deploy --dry-run"
            ),
            f"MCP package dry-run build script is missing: {relative}",
        )

    ci_workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    for required_ci_gate in (
        "ruff check src/ospo resources/build/ospo_build_backend.py resources/dev/tests resources/dev/scripts",
        "mypy src/ospo",
        "npm audit --omit=dev --audit-level=moderate",
        "npm run typecheck",
        "npm run build",
        "GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}",
    ):
        check.require(required_ci_gate in ci_workflow, f"CI gate is missing: {required_ci_gate}")

    release_workflow = (root / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    for required_release_gate in (
        "sha256sum dist/* > SHA256SUMS",
        "actions/attest@a1948c3f048ba23858d222213b7c278aabede763",
        "subject-path: dist/*",
        "environment: pypi",
        "id-token: write",
    ):
        check.require(required_release_gate in release_workflow, f"release gate is missing: {required_release_gate}")

    dependabot = (root / ".github" / "dependabot.yml").read_text(encoding="utf-8")
    for relative in MCP_PACKAGES:
        check.require(f"directory: /{relative}" in dependabot, f"Dependabot omits MCP package: {relative}")

    skill = root / "src" / "skills" / "recon-rodeo"
    claude = root / "src" / ".claude" / "agents"
    codex = root / "src" / ".codex" / "agents"
    package = root / "src" / "ospo"
    check.require((package / "__init__.py").is_file(), "src-layout ospo package is missing")
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

    ledger_path = root / "resources" / "docs" / "research" / "provenance.csv"
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
        path
        for path in directory.iterdir()
        if path.is_file() and (path.suffix == ".whl" or path.name.endswith(".tar.gz"))
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
                    "/resources/docs/research/" in f"/{member}"
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
                "resources/docs/evidence-and-provenance.md",
                "resources/docs/privacy-and-data-handling.md",
                "resources/docs/release-process.md",
                "resources/docs/responsible-use.md",
                "resources/docs/security-model.md",
                "resources/docs/research/README.md",
                "resources/docs/research/provenance.csv",
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
