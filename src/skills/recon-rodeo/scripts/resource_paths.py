"""Resolve Green Ink resources in source checkouts and installed wheels."""

from __future__ import annotations

import importlib
from pathlib import Path


def _package_directory(name: str) -> Path:
    module = importlib.import_module(name)
    module_file = getattr(module, "__file__", None)
    if not module_file:
        raise RuntimeError(f"Packaged resource module has no filesystem path: {name}")
    return Path(module_file).resolve().parent


def resource_directories() -> tuple[Path, Path]:
    """Return reference/template roots for either supported installation mode."""
    source_root = Path(__file__).resolve().parent.parent
    source_references = source_root / "references"
    source_templates = source_root / "templates"
    if source_references.is_dir() and source_templates.is_dir():
        return source_references, source_templates

    try:
        return (
            _package_directory("green_ink_references"),
            _package_directory("green_ink_templates"),
        )
    except (ImportError, RuntimeError) as exc:
        raise RuntimeError(
            "Green Ink references/templates are missing from this installation. "
            "Reinstall a wheel that includes the packaged resource modules."
        ) from exc
