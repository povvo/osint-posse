"""Build hooks for copying canonical release resources into the wheel."""

from __future__ import annotations

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).resolve().parent


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
                    "*:Zone.Identifier",
                ),
            )


setup(cmdclass={"build_py": BuildWithResources})
