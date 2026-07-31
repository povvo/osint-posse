"""Canonical resource and installation path resolution for ospo."""

from dataclasses import dataclass
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_PROJECT_ROOT = _PKG.parents[1]
_BUNDLED = _PKG / "data"


@dataclass(frozen=True)
class ReleaseResources:
    skill: Path
    claude_agents: Path
    codex_agents: Path


@dataclass(frozen=True)
class InstallPaths:
    root: Path
    skill: Path
    claude_agents: Path
    codex_agents: Path
    ownership: Path


def release_resources() -> ReleaseResources:
    """Resolve wheel resources, with one explicit source-checkout fallback."""
    bundled = ReleaseResources(
        skill=_BUNDLED / "recon-rodeo",
        claude_agents=_BUNDLED / "agents" / "claude",
        codex_agents=_BUNDLED / "agents" / "codex",
    )
    if all(path.is_dir() for path in bundled.__dict__.values()):
        return bundled

    source = ReleaseResources(
        skill=_PROJECT_ROOT / "src" / "skills" / "recon-rodeo",
        claude_agents=_PROJECT_ROOT / "src" / ".claude" / "agents",
        codex_agents=_PROJECT_ROOT / "src" / ".codex" / "agents",
    )
    if all(path.is_dir() for path in source.__dict__.values()):
        return source
    raise RuntimeError("osint-posse release resources are incomplete; reinstall from a verified wheel.")


def install_paths(scope: str, root: Path | None = None) -> InstallPaths:
    """Return project-scoped paths by default or explicit user-scoped paths."""
    if scope not in {"project", "user"}:
        raise ValueError("scope must be 'project' or 'user'")
    base = (root or (Path.cwd() if scope == "project" else Path.home())).expanduser().resolve()
    if scope == "project":
        return InstallPaths(
            root=base,
            skill=base / ".agents" / "skills" / "recon-rodeo",
            claude_agents=base / ".claude" / "agents",
            codex_agents=base / ".codex" / "agents",
            ownership=base / ".ospo" / "ownership.json",
        )
    return InstallPaths(
        root=base,
        skill=base / ".agents" / "skills" / "recon-rodeo",
        claude_agents=base / ".claude" / "agents",
        codex_agents=base / ".codex" / "agents",
        ownership=base / ".config" / "ospo" / "ownership.json",
    )

HOME = Path.home()
CONFIG_DIR = HOME / ".config" / "ospo"
CONFIG_FILE = CONFIG_DIR / "config.toml"

# Compatibility constants for status output. Lifecycle commands resolve scope at call time.
AGENTS_SKILLS = Path.cwd() / ".agents" / "skills" / "recon-rodeo"
CLAUDE_AGENTS = Path.cwd() / ".claude" / "agents"
CODEX_AGENTS = Path.cwd() / ".codex" / "agents"
