#!/usr/bin/env python3
"""Project-scoped case state for the Green Ink task runner."""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from resource_paths import resource_directories

SKILL_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = SKILL_ROOT.parents[1]
_REFERENCES, _TEMPLATES = resource_directories()
NOTEBOOK_TEMPLATE = _TEMPLATES / "working" / "investigation-notebook.md"

STATE_DIRNAME = ".green-ink"
CASES_DIRNAME = "cases"
ACTIVE_CASE_FILENAME = "active-case"
PROGRESS_FILENAME = "progress.json"
NOTEBOOK_FILENAME = "investigation-notebook.md"

CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
JsonObject = dict[str, Any]


class CaseStateError(RuntimeError):
    """Raised when a case workspace or state file is unsafe or malformed."""


@dataclass(frozen=True)
class CaseContext:
    """Resolved paths for one investigation inside one user workspace."""

    workspace: Path
    investigation_id: str
    state_root: Path
    case_dir: Path
    progress_file: Path
    notebook_path: Path
    active_case_file: Path

    def display(self, path: Path) -> str:
        """Return a stable workspace-relative path when possible."""
        try:
            return str(path.relative_to(self.workspace))
        except ValueError:
            return str(path)


def _is_link_or_reparse(path: Path) -> bool:
    """Return whether path is a symlink, Windows junction, or reparse point."""
    try:
        result = path.lstat()
    except FileNotFoundError:
        return False

    attributes = getattr(result, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(result.st_mode) or bool(attributes & reparse_flag)


def _is_regular_file(path: Path) -> bool:
    """Return whether an existing path is a non-link regular file."""
    try:
        return stat.S_ISREG(path.lstat().st_mode) and not _is_link_or_reparse(path)
    except FileNotFoundError:
        return False


def _is_directory(path: Path) -> bool:
    """Return whether an existing path is a non-link directory."""
    try:
        return stat.S_ISDIR(path.lstat().st_mode) and not _is_link_or_reparse(path)
    except FileNotFoundError:
        return False


def _is_within(path: Path, parent: Path) -> bool:
    """Return whether an already-resolved path is contained by parent."""
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _require_contained(path: Path, parent: Path, *, description: str) -> Path:
    """Resolve a path and prove that it remains below parent."""
    resolved_parent = parent.resolve(strict=True)
    resolved_path = path.resolve(strict=False)

    if not _is_within(resolved_path, resolved_parent):
        raise CaseStateError(
            f"{description} resolves outside the approved workspace: {resolved_path}"
        )
    return resolved_path


def _require_safe_directory(
    path: Path,
    *,
    parent: Path,
    description: str,
    create: bool = False,
) -> Path:
    """Validate or create a contained non-link directory."""
    _require_contained(path, parent, description=description)

    if path.exists():
        if not _is_directory(path):
            raise CaseStateError(
                f"{description} must be a non-link directory: {path}"
            )
    elif create:
        path.mkdir(mode=0o700)
    else:
        raise FileNotFoundError(f"{description} does not exist: {path}")

    return _require_contained(path, parent, description=description)


def validate_case_id(value: str) -> str:
    """Validate an investigation identifier before using it as a path component."""
    case_id = value.strip()

    if not CASE_ID_RE.fullmatch(case_id):
        raise CaseStateError(
            "Investigation ID must be 1-128 characters using only letters, "
            "numbers, dots, underscores, or hyphens; it must begin with a "
            "letter or number."
        )

    if case_id in {".", ".."}:
        raise CaseStateError("Investigation ID cannot be '.' or '..'.")

    return case_id


def resolve_workspace(explicit: str | Path | None = None) -> Path:
    """Resolve a user-owned workspace and reject installed-plugin locations."""
    raw: str | Path = (
        explicit
        if explicit is not None
        else os.environ.get("GREEN_INK_WORKSPACE") or Path.cwd()
    )
    workspace = Path(raw).expanduser()

    if workspace.exists() and not workspace.is_dir():
        raise CaseStateError(f"Workspace is not a directory: {workspace}")

    workspace.mkdir(parents=True, exist_ok=True)
    workspace = workspace.resolve(strict=True)

    if _is_link_or_reparse(workspace):
        raise CaseStateError(
            f"Workspace must not be a symlink or reparse point: {workspace}"
        )

    plugin_root = PLUGIN_ROOT.resolve(strict=True)
    if _is_within(workspace, plugin_root):
        raise CaseStateError(
            "Refusing to store mutable investigation state inside the installed "
            f"plugin tree ({plugin_root}). Run from the user's project directory "
            "or pass --workspace /path/to/project."
        )

    return workspace


def _normalise_workspace(workspace: Path) -> Path:
    """Reapply workspace protections for all public programmatic entry points."""
    return resolve_workspace(workspace)


def _state_paths(workspace: Path) -> tuple[Path, Path, Path]:
    """Return validated workspace, state root, and cases root paths."""
    workspace = _normalise_workspace(workspace)
    state_root = workspace / STATE_DIRNAME
    cases_root = state_root / CASES_DIRNAME

    _require_contained(state_root, workspace, description="State directory")
    _require_contained(cases_root, workspace, description="Cases directory")

    return workspace, state_root, cases_root


def _ensure_state_layout(workspace: Path) -> tuple[Path, Path, Path]:
    """Create and validate the non-link state directory hierarchy."""
    workspace, state_root, cases_root = _state_paths(workspace)

    _require_safe_directory(
        state_root,
        parent=workspace,
        description="State directory",
        create=True,
    )
    _require_safe_directory(
        cases_root,
        parent=workspace,
        description="Cases directory",
        create=True,
    )

    return workspace, state_root, cases_root


def _safe_state_paths(workspace: Path, investigation_id: str) -> CaseContext:
    """Construct contained state paths without creating a case directory."""
    workspace, state_root, cases_root = _ensure_state_layout(workspace)
    case_id = validate_case_id(investigation_id)
    case_dir = cases_root / case_id

    _require_contained(case_dir, cases_root, description="Case directory")

    return CaseContext(
        workspace=workspace,
        investigation_id=case_id,
        state_root=state_root,
        case_dir=case_dir,
        progress_file=case_dir / PROGRESS_FILENAME,
        notebook_path=case_dir / NOTEBOOK_FILENAME,
        active_case_file=state_root / ACTIVE_CASE_FILENAME,
    )


def _assert_safe_context(context: CaseContext, *, require_case: bool) -> None:
    """Revalidate a context immediately before filesystem access or mutation."""
    workspace, state_root, cases_root = _state_paths(context.workspace)

    if workspace != context.workspace or state_root != context.state_root:
        raise CaseStateError("Case context no longer resolves to its original workspace.")

    if state_root.exists() and not _is_directory(state_root):
        raise CaseStateError(f"Unsafe state directory: {state_root}")
    if cases_root.exists() and not _is_directory(cases_root):
        raise CaseStateError(f"Unsafe cases directory: {cases_root}")

    _require_contained(context.case_dir, cases_root, description="Case directory")
    if require_case and not _is_directory(context.case_dir):
        raise CaseStateError(
            f"Investigation '{context.investigation_id}' is not initialized in "
            f"{context.workspace}."
        )

    for path, description in (
        (context.progress_file, "Progress file"),
        (context.notebook_path, "Notebook"),
        (context.active_case_file, "Active-case file"),
    ):
        _require_contained(path, workspace, description=description)
        if path.exists() and not _is_regular_file(path):
            raise CaseStateError(f"{description} must be a regular file: {path}")


def _atomic_write_text(path: Path, text: str) -> None:
    """Atomically replace a UTF-8 regular file within an existing safe directory."""
    if not _is_directory(path.parent):
        raise CaseStateError(
            f"Refusing to write beneath missing or unsafe directory: {path.parent}"
        )
    if path.exists() and not _is_regular_file(path):
        raise CaseStateError(f"Refusing to replace non-regular file: {path}")

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary_path, path)

        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            return

        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary_path.unlink(missing_ok=True)


def _validate_progress(value: Any) -> JsonObject:
    """Validate and normalize persisted task progress."""
    if not isinstance(value, dict):
        raise CaseStateError("Progress state must be a JSON object.")

    completed = value.get("completed")
    current_index = value.get("current_index")
    completion_records = value.get("completion_records", {})

    if (
        not isinstance(completed, list)
        or any(not isinstance(item, str) or not item for item in completed)
        or len(completed) != len(set(completed))
    ):
        raise CaseStateError(
            "Progress field 'completed' must be a list of unique non-empty task IDs."
        )

    if isinstance(current_index, bool) or not isinstance(current_index, int):
        raise CaseStateError(
            "Progress field 'current_index' must be a non-negative integer."
        )
    if current_index < 0:
        raise CaseStateError(
            "Progress field 'current_index' must be a non-negative integer."
        )

    if not isinstance(completion_records, dict):
        raise CaseStateError(
            "Progress field 'completion_records' must be an object keyed by task ID."
        )

    if any(
        not isinstance(task_id, str)
        or not task_id
        or not isinstance(record, dict)
        for task_id, record in completion_records.items()
    ):
        raise CaseStateError(
            "Every completion record must be an object keyed by a non-empty task ID."
        )

    orphaned = sorted(set(completion_records) - set(completed))
    if orphaned:
        raise CaseStateError(
            "Completion records exist for tasks not marked complete: "
            + ", ".join(orphaned)
        )

    return {
        "completed": list(completed),
        "current_index": current_index,
        "completion_records": completion_records,
    }


def initial_progress() -> JsonObject:
    """Return a new empty task-progress document."""
    return {"completed": [], "current_index": 0, "completion_records": {}}


def _read_notebook_template() -> str:
    """Read the installed notebook template as UTF-8 text."""
    if not _is_regular_file(NOTEBOOK_TEMPLATE):
        raise CaseStateError(
            f"Notebook template must be a regular file: {NOTEBOOK_TEMPLATE}"
        )

    try:
        return NOTEBOOK_TEMPLATE.read_text(encoding="utf-8")
    except OSError as exc:
        raise CaseStateError(
            f"Could not read notebook template {NOTEBOOK_TEMPLATE}: {exc}"
        ) from exc


def initialise_case(
    workspace: Path,
    investigation_id: str,
) -> tuple[CaseContext, bool]:
    """Create or select one case without overwriting notes or progress."""
    context = _safe_state_paths(workspace, investigation_id)
    cases_root = context.state_root / CASES_DIRNAME

    case_created = not context.case_dir.exists()
    _require_safe_directory(
        context.case_dir,
        parent=cases_root,
        description="Case directory",
        create=True,
    )
    _assert_safe_context(context, require_case=True)

    if not context.progress_file.exists():
        save_progress(context, initial_progress())

    if not context.notebook_path.exists():
        _atomic_write_text(context.notebook_path, _read_notebook_template())

    _atomic_write_text(context.active_case_file, context.investigation_id + "\n")
    return context, case_created


def select_case(
    workspace: Path,
    explicit_investigation_id: str | None = None,
) -> CaseContext:
    """Resolve an explicit, environment, or persisted active case selection."""
    workspace, state_root, _cases_root = _state_paths(workspace)
    active_case_file = state_root / ACTIVE_CASE_FILENAME

    selected = explicit_investigation_id or os.environ.get(
        "GREEN_INK_INVESTIGATION_ID"
    )

    if not selected and active_case_file.exists():
        if not _is_regular_file(active_case_file):
            raise CaseStateError(
                f"Active-case selection must be a regular file: {active_case_file}"
            )
        try:
            selected = active_case_file.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise CaseStateError(
                f"Could not read active case selection {active_case_file}: {exc}"
            ) from exc

    if not selected:
        raise CaseStateError(
            "No investigation is selected. Initialize one with "
            "`python3 scripts/task_runner.py init <investigation-id> "
            "--workspace /path/to/project`."
        )

    context = _safe_state_paths(workspace, selected)
    _assert_safe_context(context, require_case=True)
    return context


def list_cases(workspace: Path) -> tuple[list[str], str | None]:
    """List initialized safe case directories and the validated active selection."""
    workspace, state_root, cases_root = _state_paths(workspace)
    active_case_file = state_root / ACTIVE_CASE_FILENAME
    active: str | None = None

    if active_case_file.exists():
        if not _is_regular_file(active_case_file):
            raise CaseStateError(
                f"Active-case selection must be a regular file: {active_case_file}"
            )
        try:
            selected = active_case_file.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise CaseStateError(
                f"Could not read active case selection {active_case_file}: {exc}"
            ) from exc
        active = validate_case_id(selected) if selected else None

    if not cases_root.exists():
        return [], active
    if not _is_directory(cases_root):
        raise CaseStateError(f"Cases directory must be a non-link directory: {cases_root}")

    cases: list[str] = []
    for path in cases_root.iterdir():
        if not _is_directory(path) or not CASE_ID_RE.fullmatch(path.name):
            continue

        manifest_progress = path / PROGRESS_FILENAME
        if manifest_progress.exists() and not _is_regular_file(manifest_progress):
            raise CaseStateError(
                f"Case contains unsafe progress state: {manifest_progress}"
            )
        cases.append(path.name)

    return sorted(cases), active


def load_progress(context: CaseContext) -> JsonObject:
    """Load validated progress; malformed or unsafe state fails closed."""
    _assert_safe_context(context, require_case=True)

    if not context.progress_file.exists():
        return initial_progress()

    try:
        data = json.loads(context.progress_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CaseStateError(
            f"Malformed progress JSON in {context.progress_file}: {exc}"
        ) from exc
    except OSError as exc:
        raise CaseStateError(
            f"Could not read progress file {context.progress_file}: {exc}"
        ) from exc

    return _validate_progress(data)


def save_progress(context: CaseContext, state: JsonObject) -> None:
    """Validate and atomically persist one case's progress document."""
    _assert_safe_context(context, require_case=True)
    validated = _validate_progress(state)

    _atomic_write_text(
        context.progress_file,
        json.dumps(validated, indent=2, sort_keys=True) + "\n",
    )


def ensure_notebook(context: CaseContext) -> Path:
    """Create a notebook from the installed template only when it is absent."""
    _assert_safe_context(context, require_case=True)

    if context.notebook_path.exists():
        return context.notebook_path

    _atomic_write_text(context.notebook_path, _read_notebook_template())
    return context.notebook_path