#!/usr/bin/env python3
"""
Green Ink task runner.

Sequential workflow runner for the 56-task investigation pipeline. Mutable
progress and notebook state are stored per investigation in a user-owned
workspace, never inside the installed plugin.

Examples:
    python3 task_runner.py init INV-example --workspace /path/to/project
    python3 task_runner.py next --workspace /path/to/project
    python3 task_runner.py done --workspace /path/to/project
    python3 task_runner.py status --workspace /path/to/project
    python3 task_runner.py reset --workspace /path/to/project
    python3 task_runner.py jump t6.2 --workspace /path/to/project
    python3 task_runner.py peek t9.1 --workspace /path/to/project
    python3 task_runner.py notebook --workspace /path/to/project
    python3 task_runner.py cases --workspace /path/to/project

The workspace can also be set with GREEN_INK_WORKSPACE. Select a case with
--investigation-id/--case, GREEN_INK_INVESTIGATION_ID, or the active case
written by the init command.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Import shared configuration and state helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from case_state import (  # noqa: E402
    CaseContext,
    CaseStateError,
    ensure_notebook,
    initialise_case,
    list_cases,
    load_progress,
    resolve_workspace,
    save_progress,
    select_case,
)
from config import (  # noqa: E402
    PHASES,
    STEP_MCP_TOOLS,
    STEP_SCRIPTS,
    STEP_TEMPLATES,
)
from resource_paths import resource_directories  # noqa: E402

# ---------------------------------------------------------------------------
# Immutable plugin resources
# ---------------------------------------------------------------------------
SKILL_ROOT = Path(__file__).resolve().parent.parent
REFERENCES, TEMPLATES = resource_directories()

# task_runner.py is a workflow state machine. It never installs packages.
# Use scripts/setup.py or package extras from pyproject.toml for explicit setup.


# ---------------------------------------------------------------------------
# Task discovery and ordering
# ---------------------------------------------------------------------------
TASK_RE = re.compile(r"^t(\d+)\.(\d+)([ab]?)\.md$")
SCRIPT_TOOL_NAMES = {
    "chronological_matrix.py": "chronology",
    "content_archiver.py": "content-archiver",
    "corporate_intel.py": "corporate-intel",
    "domain_intel.py": "domain-intel",
    "entity_resolver.py": "entity-resolver",
    "evidence_preservation.py": "evidence-preservation",
    "financial_analysis.py": "financial-analysis",
    "geolocation.py": "geolocation",
    "network_graph.py": "network-graph",
    "report_generator.py": "report-generator",
    "sanctions_screen.py": "sanctions-screen",
    "source_grader.py": "source-grader",
    "username_enum.py": "username-enum",
}


def parse_task_id(filename: str) -> tuple[int, int, str] | None:
    """Extract (step, subtask, suffix) from a task filename."""
    match = TASK_RE.match(filename)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), match.group(3)


def task_sort_key(entry: dict) -> tuple:
    """Sort by phase, step, subtask, then suffix."""
    suffix_order = {"a": 0, "b": 1, "": 2}
    phase_number = PHASES[entry["phase"]]["number"]
    return (
        phase_number,
        entry["step"],
        entry["subtask"],
        suffix_order.get(entry["suffix"], 3),
    )


def task_display_id(entry: dict) -> str:
    """Return a task ID such as t3.1a or t9.2."""
    return f"t{entry['step']}.{entry['subtask']}{entry['suffix']}"


def discover_tasks() -> list[dict]:
    """Walk references/ and build the ordered task list."""
    tasks: list[dict] = []
    for phase_folder in PHASES:
        phase_dir = REFERENCES / phase_folder
        if not phase_dir.is_dir():
            continue
        for path in phase_dir.iterdir():
            parsed = parse_task_id(path.name)
            if parsed is None:
                continue
            step, subtask, suffix = parsed
            tasks.append(
                {
                    "id": task_display_id(
                        {"step": step, "subtask": subtask, "suffix": suffix}
                    ),
                    "step": step,
                    "subtask": subtask,
                    "suffix": suffix,
                    "phase": phase_folder,
                    "file": str(path.relative_to(SKILL_ROOT)),
                    "abs_path": str(path),
                }
            )
    tasks.sort(key=task_sort_key)
    return tasks


def validate_progress_for_tasks(state: dict, tasks: list[dict]) -> None:
    """Reject state that cannot be reconciled with the installed workflow."""
    task_ids = {task["id"] for task in tasks}
    unknown = sorted(set(state["completed"]) - task_ids)
    if unknown:
        raise CaseStateError(
            "Progress contains task IDs that are not present in this plugin version: "
            + ", ".join(unknown)
        )
    if state["current_index"] > len(tasks):
        raise CaseStateError(
            f"Progress current_index {state['current_index']} exceeds the "
            f"{len(tasks)} available tasks."
        )
    ordered_ids = [task["id"] for task in tasks]
    expected_prefix = ordered_ids[: state["current_index"]]
    if state["completed"] != expected_prefix:
        raise CaseStateError(
            "Progress must be a contiguous ordered prefix of the installed workflow. "
            "A future task cannot be selected or completed before its predecessors."
        )
    completion_records = state.get("completion_records", {})
    missing_records = [task_id for task_id in state["completed"] if task_id not in completion_records]
    if missing_records:
        raise CaseStateError(
            "Completed tasks lack verified completion records: "
            + ", ".join(missing_records)
            + ". Re-audit this legacy progress before continuing."
        )


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
def print_divider(char: str = "-", width: int = 72) -> None:
    print(char * width)


def print_task_card(
    task: dict,
    tasks: list[dict],
    state: dict,
    context: CaseContext,
    show_content: bool = True,
) -> None:
    """Print a full task card with context, resources, and file content."""
    task_id = task["id"]
    phase_meta = PHASES[task["phase"]]
    step = task["step"]
    index = next(i for i, candidate in enumerate(tasks) if candidate["id"] == task_id)
    total = len(tasks)

    print()
    print_divider("=")
    print(f"  TASK {task_id.upper()}")
    print(f"  Investigation: {context.investigation_id}")
    print(f"  Workspace: {context.workspace}")
    print(f"  Phase {phase_meta['number']}: {phase_meta['title']}")
    print(f"  Intelligence Cycle: {phase_meta['cycle_stage']}")
    print(f"  Progress: {len(state['completed'])}/{total} complete")
    print(f"  Notebook: {context.display(context.notebook_path)}")
    print_divider("=")

    scripts = STEP_SCRIPTS.get(step, [])
    if scripts:
        print("\n  Scripts required (MUST execute via bash before calling done):")
        for script in scripts:
            path = SKILL_ROOT / "scripts" / script
            exists = "OK" if path.exists() else "NO"
            print(f"    {exists} python3 scripts/{script}")

    templates = STEP_TEMPLATES.get(step, [])
    if templates:
        print("\n  Templates:")
        for template in templates:
            path = TEMPLATES / template
            exists = "OK" if path.exists() else "NO"
            print(f"    {exists} templates/{template}")

    tools = STEP_MCP_TOOLS.get(step, [])
    if tools:
        print("\n  MCP/Tools:")
        for tool in tools:
            print(f"    -> {tool}")

    if show_content:
        print()
        print_divider()
        print(f"  FILE: {task['file']}")
        print_divider()
        try:
            content = Path(task["abs_path"]).read_text(encoding="utf-8").strip()
            if not content:
                print("  [EMPTY FILE - needs content]")
            else:
                print(content)
        except OSError as exc:
            print(f"  [Error reading file: {exc}]")

    print()
    print_divider("=")
    if index + 1 < total:
        next_task = tasks[index + 1]
        print(f"  Next up: {next_task['id'].upper()} ({next_task['file']})")
    else:
        print("  This is the final task.")
    print()


def print_status(tasks: list[dict], state: dict, context: CaseContext) -> None:
    """Print a progress overview grouped by phase."""
    total = len(tasks)
    done = set(state["completed"])
    current_index = state["current_index"]
    current_id = tasks[current_index]["id"] if current_index < total else None

    print()
    print_divider("=")
    print(f"  INVESTIGATION: {context.investigation_id}")
    print(f"  PROGRESS: {len(done)}/{total} tasks")
    print_divider("=")

    for phase_key, phase_meta in PHASES.items():
        phase_tasks = [task for task in tasks if task["phase"] == phase_key]
        phase_done = sum(1 for task in phase_tasks if task["id"] in done)
        percentage = int(100 * phase_done / len(phase_tasks)) if phase_tasks else 0

        bar_width = 20
        filled = (
            int(bar_width * phase_done / len(phase_tasks)) if phase_tasks else 0
        )
        bar = "#" * filled + "." * (bar_width - filled)

        print(f"\n  Phase {phase_meta['number']}: {phase_meta['title']}")
        print(f"  {bar} {phase_done}/{len(phase_tasks)} ({percentage}%)")

        for task in phase_tasks:
            task_id = task["id"]
            if task_id in done:
                marker = "  [x]"
            elif task_id == current_id:
                marker = "  ->"
            else:
                marker = "    "
            print(f"    {marker} {task_id}")

    print()
    print_divider("=")
    if current_id:
        print(f"  Current position: {current_id.upper()}")
    else:
        print("  All tasks complete.")
    print()


# ---------------------------------------------------------------------------
# Verification gate
# ---------------------------------------------------------------------------
PROCEDURE_RE = re.compile(r"^##\s+Procedure\s*$", re.IGNORECASE)
SECTION_RE = re.compile(r"^###\s+\d+\.?\s*(.+)$")
NUMBERED_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.+)$")


def checklist_label(value: str) -> str:
    """Normalise one Markdown requirement for compact terminal display."""
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = value.replace("**", "")
    return re.sub(r"\s+", " ", value).strip()


def extract_checklist(task: dict) -> list[dict]:
    """Parse the shipped ``## Procedure`` format into checklist items.

    Task cards use either top-level numbered steps or numbered ``###``
    sections containing dash bullets.  Only procedure content is eligible so
    descriptive prose cannot accidentally satisfy the completion gate.
    """
    try:
        content = Path(task["abs_path"]).read_text(encoding="utf-8").strip()
    except OSError:
        return []

    if not content:
        return []

    sections: list[dict] = []
    current_section: dict | None = None
    in_procedure = False

    def ensure_section() -> dict:
        nonlocal current_section
        if current_section is None:
            current_section = {"title": "Procedure", "items": []}
            sections.append(current_section)
        return current_section

    for line in content.splitlines():
        stripped = line.strip()
        if not in_procedure:
            if PROCEDURE_RE.match(stripped):
                in_procedure = True
            continue

        if stripped.startswith("## "):
            break

        section_match = SECTION_RE.match(stripped)
        if section_match:
            current_section = {
                "title": checklist_label(section_match.group(1)),
                "items": [],
            }
            sections.append(current_section)
            continue

        numbered_match = NUMBERED_RE.match(line)
        if numbered_match:
            label = checklist_label(numbered_match.group(2))
            if label:
                ensure_section()["items"].append(
                    f"{numbered_match.group(1)}. {label}"
                )
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            label = checklist_label(bullet_match.group(1))
            if label:
                ensure_section()["items"].append(label)

    return [section for section in sections if section["items"]]


def completion_requirements(task: dict) -> dict[str, str]:
    """Return stable IDs and labels for every mandatory procedure item."""
    requirements: dict[str, str] = {}
    for section_index, section in enumerate(extract_checklist(task), start=1):
        for item_index, item in enumerate(section["items"], start=1):
            requirements[f"procedure.{section_index}.{item_index}"] = item
    return requirements


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_evidence_file(raw: str, context: CaseContext) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = context.workspace / path
    path = path.resolve()
    try:
        path.relative_to(context.workspace)
    except ValueError as exc:
        raise CaseStateError(
            f"Evidence file must be inside the investigation workspace: {path}"
        ) from exc
    if not path.is_file() or path.is_symlink() or path.stat().st_size == 0:
        raise CaseStateError(f"Evidence file is missing, empty, or unsafe: {path}")
    return path


def _validate_evidence_list(value: object, label: str, context: CaseContext) -> list[dict]:
    if not isinstance(value, list) or not value:
        raise CaseStateError(f"{label} requires at least one evidence item.")
    validated: list[dict] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise CaseStateError(f"{label} evidence item {index} must be an object.")
        kind = item.get("kind")
        if kind == "file":
            raw_path = item.get("path")
            if not isinstance(raw_path, str) or not raw_path.strip():
                raise CaseStateError(f"{label} file evidence item {index} requires path.")
            path = _resolve_evidence_file(raw_path, context)
            validated.append(
                {"kind": "file", "path": context.display(path), "sha256": _sha256_file(path)}
            )
        elif kind in {"note", "record"}:
            content = item.get("value")
            if not isinstance(content, str) or len(content.strip()) < 3:
                raise CaseStateError(
                    f"{label} {kind} evidence item {index} requires a non-empty value."
                )
            validated.append({"kind": kind, "value": content.strip()})
        else:
            raise CaseStateError(
                f"{label} evidence item {index} has invalid kind; use file, note, or record."
            )
    return validated


def completion_manifest_template(task: dict) -> dict:
    """Build the exact manifest shape required by ``done`` for one task."""
    step = task["step"]
    return {
        "schema_version": "1.0",
        "task_id": task["id"],
        "requirements": {
            requirement_id: {
                "label": label,
                "evidence": [{"kind": "note", "value": ""}],
            }
            for requirement_id, label in completion_requirements(task).items()
        },
        "scripts": {
            name: {
                "receipt_path": "",
                "evidence": [],
            }
            for name in STEP_SCRIPTS.get(step, [])
        },
        "templates": {
            name: {"output_paths": []}
            for name in STEP_TEMPLATES.get(step, [])
        },
        "tools": {
            name: {"evidence": []}
            for name in STEP_MCP_TOOLS.get(step, [])
        },
        "notebook": {"updated": False, "evidence": []},
    }


def validate_completion_manifest(
    path: Path,
    task: dict,
    state: dict,
    context: CaseContext,
) -> dict:
    """Validate all procedure, output, tool, and notebook evidence without writes."""
    try:
        raw_bytes = path.read_bytes()
        manifest = json.loads(raw_bytes)
    except FileNotFoundError as exc:
        raise CaseStateError(f"Completion manifest not found: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise CaseStateError(f"Could not read completion manifest {path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise CaseStateError("Completion manifest must be a JSON object.")
    if manifest.get("schema_version") != "1.0":
        raise CaseStateError("Completion manifest schema_version must be '1.0'.")
    if manifest.get("task_id") != task["id"]:
        raise CaseStateError(
            f"Completion manifest task_id must be {task['id']!r}."
        )

    expected_requirements = completion_requirements(task)
    if not expected_requirements:
        raise CaseStateError(
            f"No mandatory procedure requirements could be extracted from {task['file']}."
        )
    supplied_requirements = manifest.get("requirements")
    if not isinstance(supplied_requirements, dict):
        raise CaseStateError("Completion manifest requirements must be an object.")
    if set(supplied_requirements) != set(expected_requirements):
        missing = sorted(set(expected_requirements) - set(supplied_requirements))
        extra = sorted(set(supplied_requirements) - set(expected_requirements))
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if extra:
            detail.append("unknown " + ", ".join(extra))
        raise CaseStateError("Requirement IDs do not match the task card: " + "; ".join(detail))

    evidence_summary: dict[str, list[dict]] = {}
    for requirement_id, expected_label in expected_requirements.items():
        entry = supplied_requirements[requirement_id]
        if not isinstance(entry, dict):
            raise CaseStateError(f"Requirement {requirement_id} must be an object.")
        if entry.get("label") != expected_label:
            raise CaseStateError(
                f"Requirement {requirement_id} label does not match the installed task card."
            )
        evidence_summary[requirement_id] = _validate_evidence_list(
            entry.get("evidence"), f"Requirement {requirement_id}", context
        )

    step = task["step"]
    supplied_scripts = manifest.get("scripts", {})
    expected_scripts = set(STEP_SCRIPTS.get(step, []))
    script_summary: dict[str, dict] = {}
    if not isinstance(supplied_scripts, dict) or set(supplied_scripts) != expected_scripts:
        raise CaseStateError("Script evidence does not exactly match the task's required scripts.")
    for name, entry in supplied_scripts.items():
        if not isinstance(entry, dict):
            raise CaseStateError(f"Required script {name} must be an object.")
        raw_receipt = entry.get("receipt_path")
        if not isinstance(raw_receipt, str) or not raw_receipt.strip():
            raise CaseStateError(f"Required script {name} needs a Green Ink receipt path.")
        receipt_path = _resolve_evidence_file(raw_receipt, context)
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CaseStateError(f"Invalid execution receipt for {name}: {exc}") from exc
        expected_tool = SCRIPT_TOOL_NAMES.get(name)
        if expected_tool is None:
            raise CaseStateError(f"Required script {name} has no allow-listed CLI tool mapping.")
        if (
            not isinstance(receipt, dict)
            or receipt.get("schema_version") != "2.0"
            or receipt.get("tool_name") != expected_tool
            or receipt.get("investigation_id") != context.investigation_id
            or receipt.get("task_id") != task["id"]
            or not isinstance(receipt.get("run_id"), str)
            or receipt.get("exit_code") != 0
            or receipt.get("workflow_progress_accessed") is not False
        ):
            raise CaseStateError(
                f"Execution receipt for {name} does not prove a successful standalone {expected_tool} run."
            )
        receipt_digest = _sha256_file(receipt_path)
        used_receipts = {
            digest
            for record in state["completion_records"].values()
            for digest in record.get("receipt_sha256", {}).values()
        }
        if receipt_digest in used_receipts:
            raise CaseStateError(f"Execution receipt for {name} has already been used by another task.")
        script_summary[name] = {
            "receipt_path": context.display(receipt_path),
            "receipt_sha256": receipt_digest,
            "evidence": _validate_evidence_list(
                entry.get("evidence"), f"Required script {name}", context
            ),
        }

    supplied_templates = manifest.get("templates", {})
    expected_templates = set(STEP_TEMPLATES.get(step, []))
    template_summary: dict[str, list[dict]] = {}
    if not isinstance(supplied_templates, dict) or set(supplied_templates) != expected_templates:
        raise CaseStateError("Template outputs do not exactly match the task's required templates.")
    for name, entry in supplied_templates.items():
        if not isinstance(entry, dict):
            raise CaseStateError(f"Required template {name} must be an object.")
        output_paths = entry.get("output_paths")
        if not isinstance(output_paths, list) or not output_paths:
            raise CaseStateError(f"Required template {name} needs at least one output path.")
        template_summary[name] = []
        for raw_path in output_paths:
            if not isinstance(raw_path, str):
                raise CaseStateError(f"Required template {name} output paths must be strings.")
            output_path = _resolve_evidence_file(raw_path, context)
            template_summary[name].append(
                {"path": context.display(output_path), "sha256": _sha256_file(output_path)}
            )

    supplied_tools = manifest.get("tools", {})
    expected_tools = set(STEP_MCP_TOOLS.get(step, []))
    tool_summary: dict[str, list[dict]] = {}
    if not isinstance(supplied_tools, dict) or set(supplied_tools) != expected_tools:
        raise CaseStateError("Tool evidence does not exactly match the task's required MCP/tools.")
    for name, entry in supplied_tools.items():
        if not isinstance(entry, dict):
            raise CaseStateError(f"Required tool {name} must be an object.")
        tool_summary[name] = _validate_evidence_list(
            entry.get("evidence"), f"Required tool {name}", context
        )

    notebook = manifest.get("notebook")
    if not isinstance(notebook, dict) or notebook.get("updated") is not True:
        raise CaseStateError("The investigation notebook must be updated for this task.")
    notebook_evidence = _validate_evidence_list(
        notebook.get("evidence"), "Notebook update", context
    )
    notebook_path = context.notebook_path
    if (
        not notebook_path.is_file()
        or notebook_path.is_symlink()
        or notebook_path.stat().st_size == 0
    ):
        raise CaseStateError(
            f"Investigation notebook is missing, empty, or unsafe: {notebook_path}"
        )
    notebook_digest = _sha256_file(notebook_path)
    previous_digest = None
    if state["completed"]:
        previous_id = state["completed"][-1]
        previous_digest = state["completion_records"][previous_id].get("notebook_sha256")
    else:
        template_path = TEMPLATES / "working" / "investigation-notebook.md"
        if template_path.is_file():
            previous_digest = _sha256_file(template_path)
    if previous_digest == notebook_digest:
        raise CaseStateError(
            "The investigation notebook is byte-identical to its prior verified state."
        )

    return {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "task_card_sha256": _sha256_file(Path(task["abs_path"])),
        "notebook_sha256": notebook_digest,
        "requirements": evidence_summary,
        "scripts": script_summary,
        "receipt_sha256": {
            name: value["receipt_sha256"] for name, value in script_summary.items()
        },
        "templates": template_summary,
        "tools": tool_summary,
        "notebook_evidence": notebook_evidence,
        "requirement_count": len(expected_requirements),
        "script_count": len(expected_scripts),
        "template_count": len(expected_templates),
        "tool_count": len(expected_tools),
    }


def print_verification_gate(
    task: dict,
    state: dict,
    context: CaseContext,
) -> int:
    """Print the completed task's requirements as a verification checklist."""
    task_id = task["id"]
    phase_meta = PHASES[task["phase"]]
    step = task["step"]

    print()
    print_divider("=")
    print(f"  VERIFICATION GATE - {task_id.upper()}")
    print(f"  Investigation: {context.investigation_id}")
    print(f"  Phase {phase_meta['number']}: {phase_meta['title']}")
    print_divider("=")

    sections = extract_checklist(task)

    if not sections:
        print(f"\n  No structured checklist could be extracted from {task['file']}.")
        print("  Review the task file manually before confirming completion.")
        print()
        print_divider()
        print(f"  FILE: {task['file']}")
        print_divider()
        try:
            content = Path(task["abs_path"]).read_text(encoding="utf-8").strip()
            if content:
                lines = content.splitlines()
                for line in lines[:20]:
                    print(f"  {line}")
                if len(lines) > 20:
                    print(f"  ... ({len(lines) - 20} more lines)")
            else:
                print("  [EMPTY FILE]")
        except OSError as exc:
            print(f"  [Error: {exc}]")
        print()
        print_divider("=")
        return 0

    item_count = 0
    for section in sections:
        print(f"\n  {section['title']}")
        if section["items"]:
            for item in section["items"]:
                if item.startswith("  "):
                    print(f"      [ ] {item.strip()}")
                else:
                    print(f"    [ ] {item}")
                item_count += 1
        else:
            print("    (no specific requirements extracted)")

    scripts = STEP_SCRIPTS.get(step, [])
    templates = STEP_TEMPLATES.get(step, [])
    tools = STEP_MCP_TOOLS.get(step, [])

    if scripts or templates or tools:
        print("\n  Tooling used:")
        for script in scripts:
            print(f"    [ ] python3 scripts/{script}  -- executed and output reviewed")
        for template in templates:
            print(f"    [ ] templates/{template}")
        for tool in tools:
            print(f"    [ ] {tool}")

    print("\n  Investigation Notebook:")
    print("    [ ] Update notebook with findings from this task")
    print("    [ ] If findings materially shift the picture, call OSDb:save_notebook")
    print(f"    Notebook path: {context.display(context.notebook_path)}")

    print()
    print_divider("=")
    print(f"  {item_count} requirements to verify.")
    print("  Confirm ALL items were completed before proceeding.")
    print_divider("=")
    print()
    return item_count


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_init(workspace: Path, case_id: str) -> None:
    context, created = initialise_case(workspace, case_id)
    action = "Initialised" if created else "Selected existing"
    print(f"\n  {action} investigation: {context.investigation_id}")
    print(f"  Workspace: {context.workspace}")
    print(f"  Progress: {context.display(context.progress_file)}")
    print(f"  Notebook: {context.display(context.notebook_path)}\n")


def cmd_cases(workspace: Path) -> None:
    cases, active = list_cases(workspace)
    print(f"\n  Green Ink cases in {workspace}:")
    if not cases:
        print("    none")
    else:
        for case_id in cases:
            marker = "*" if case_id == active else " "
            print(f"  {marker} {case_id}")
    print()


def cmd_next(
    tasks: list[dict],
    state: dict,
    context: CaseContext,
) -> None:
    """Show the current task."""
    index = state["current_index"]
    if index >= len(tasks):
        print("\n  All tasks complete. Run `task_runner.py status` for overview.\n")
        return
    print_task_card(tasks[index], tasks, state, context)


def cmd_done(
    tasks: list[dict],
    state: dict,
    context: CaseContext,
    evidence_manifest: str | None,
) -> bool:
    """Mark the current task done and advance."""
    index = state["current_index"]
    if index >= len(tasks):
        print("\n  All tasks already complete.\n")
        return True

    task = tasks[index]
    task_id = task["id"]
    requirement_count = print_verification_gate(task, state, context)
    if requirement_count == 0:
        print(
            f"\n  [blocked] {task_id.upper()} was not marked complete because "
            "its procedure requirements could not be parsed."
        )
        print("  Repair the task card or parser, then run `done` again.\n")
        return False

    if not evidence_manifest:
        print(
            f"\n  [blocked] {task_id.upper()} requires a completed evidence manifest."
        )
        print(
            "  Create one with `green-ink workflow requirements --out manifest.json`, "
            "then run `green-ink workflow done --evidence-manifest manifest.json`.\n"
        )
        return False

    try:
        manifest_path = Path(evidence_manifest).expanduser().resolve()
        completion_record = validate_completion_manifest(
            manifest_path, task, state, context
        )
        completion_dir = context.case_dir / "completion-manifests"
        completion_dir.mkdir(mode=0o750, exist_ok=True)
        archived_manifest = completion_dir / f"{task_id}.json"
        submitted_bytes = manifest_path.read_bytes()
        if archived_manifest.exists():
            if archived_manifest.read_bytes() != submitted_bytes:
                raise CaseStateError(
                    f"Archived manifest already exists with different content: {archived_manifest}"
                )
        else:
            with archived_manifest.open("xb") as handle:
                handle.write(submitted_bytes)
        completion_record["manifest_path"] = context.display(archived_manifest)
    except CaseStateError as exc:
        print(f"\n  [blocked] {exc}\n", file=sys.stderr)
        return False

    if task_id not in state["completed"]:
        state["completed"].append(task_id)
    state["completion_records"][task_id] = completion_record

    state["current_index"] = index + 1
    save_progress(context, state)

    print(f"\n  [done] Marked {task_id.upper()} complete.")

    if index + 1 < len(tasks):
        print("  Loading next task...\n")
        print_task_card(tasks[index + 1], tasks, state, context)
    else:
        print(f"\n  All {len(tasks)} tasks complete.")
        print("  Run `task_runner.py status` for final overview.\n")
    return True


def cmd_jump(
    tasks: list[dict],
    state: dict,
    context: CaseContext,
    target: str,
) -> bool:
    """Jump to a specific task by ID."""
    target_clean = target.lower().strip()
    if not target_clean.startswith("t"):
        target_clean = "t" + target_clean

    index = next(
        (i for i, task in enumerate(tasks) if task["id"] == target_clean),
        None,
    )
    if index is None:
        print(f"\n  Task '{target}' not found.")
        print(f"  Available: {', '.join(task['id'] for task in tasks[:10])}...\n")
        return False

    if index != state["current_index"]:
        print(
            f"\n  [blocked] Cannot jump to {target_clean.upper()}. "
            "Workflow position is the first incomplete task; use `peek` to inspect "
            "another card without changing progress.\n",
            file=sys.stderr,
        )
        return False
    print(f"\n  Already positioned at {target_clean.upper()}.")
    print_task_card(tasks[index], tasks, state, context)
    return True


def cmd_peek(
    tasks: list[dict],
    state: dict,
    context: CaseContext,
    target: str,
) -> None:
    """Preview a task without changing position."""
    target_clean = target.lower().strip()
    if not target_clean.startswith("t"):
        target_clean = "t" + target_clean

    task = next(
        (candidate for candidate in tasks if candidate["id"] == target_clean),
        None,
    )
    if task is None:
        print(f"\n  Task '{target}' not found.\n")
        return

    print_task_card(task, tasks, state, context)


def cmd_reset(state: dict, context: CaseContext, *, force: bool) -> None:
    """Back up and reset progress for the selected investigation only."""
    if not force:
        raise CaseStateError(
            f"Reset would remove {len(state['completed'])} completion record(s) from "
            f"{context.investigation_id}; rerun with --force after reviewing the case."
        )
    backup_dir = context.case_dir / "reset-backups"
    backup_dir.mkdir(mode=0o750, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = backup_dir / f"progress-{timestamp}.json"
    shutil.copy2(context.progress_file, backup)
    state["completed"] = []
    state["current_index"] = 0
    state["completion_records"] = {}
    save_progress(context, state)
    print(
        f"\n  Progress reset for {context.investigation_id}. "
        f"Backup: {context.display(backup)}. Starting from t1.1.\n"
    )


def cmd_list(tasks: list[dict]) -> None:
    """List all task IDs grouped by phase."""
    for phase_key, phase_meta in PHASES.items():
        phase_tasks = [task for task in tasks if task["phase"] == phase_key]
        task_ids = ", ".join(task["id"] for task in phase_tasks)
        print(f"  Phase {phase_meta['number']} ({phase_key}): {task_ids}")
    print(f"\n  Total: {len(tasks)} tasks")


def cmd_notebook(context: CaseContext) -> None:
    """Print the selected investigation notebook."""
    notebook_path = ensure_notebook(context)

    print()
    print_divider("=")
    print(f"  INVESTIGATION NOTEBOOK - {context.investigation_id}")
    print(f"  {context.display(notebook_path)}")
    print_divider("=")

    try:
        content = notebook_path.read_text(encoding="utf-8").strip()
        print(content if content else "  [NOTEBOOK IS EMPTY]")
    except OSError as exc:
        print(f"  [Error reading notebook: {exc}]")

    print()
    print_divider("=")
    print("  Sync reminder: call OSDb:save_notebook after any material update.")
    print()


def cmd_requirements(
    tasks: list[dict],
    state: dict,
    target: str | None,
    output: str | None,
) -> None:
    """Print or write the exact evidence manifest required for one task."""
    if target:
        target_clean = target.lower().strip()
        if not target_clean.startswith("t"):
            target_clean = "t" + target_clean
        task = next((item for item in tasks if item["id"] == target_clean), None)
        if task is None:
            raise CaseStateError(f"Task '{target}' not found.")
    elif state["current_index"] < len(tasks):
        task = tasks[state["current_index"]]
    else:
        raise CaseStateError("All workflow tasks are already complete.")

    payload = json.dumps(completion_manifest_template(task), indent=2) + "\n"
    if output:
        out_path = Path(output).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8", newline="\n")
        print(f"  Completion manifest template written to {out_path}")
    else:
        print(payload, end="")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Green Ink project-scoped task runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="next",
        choices=[
            "init",
            "cases",
            "next",
            "done",
            "status",
            "reset",
            "jump",
            "peek",
            "list",
            "notebook",
            "requirements",
        ],
        help="Command to execute (default: next)",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Investigation ID for init, or task ID for jump/peek",
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help=(
            "User-owned project directory. Defaults to GREEN_INK_WORKSPACE "
            "or the current directory."
        ),
    )
    parser.add_argument(
        "--investigation-id",
        "--case",
        dest="investigation_id",
        default=None,
        help=(
            "Select an initialised investigation. Defaults to "
            "GREEN_INK_INVESTIGATION_ID or the workspace's active case."
        ),
    )
    parser.add_argument(
        "--evidence-manifest",
        default=None,
        help="JSON completion manifest required by done.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output path for the requirements manifest template.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Confirm a destructive, case-scoped reset after a backup is written.",
    )
    args = parser.parse_args(argv)

    try:
        workspace = resolve_workspace(args.workspace)

        if args.command == "init":
            case_id = args.investigation_id or args.target
            if not case_id:
                raise CaseStateError(
                    "init requires an investigation ID, for example "
                    "`task_runner.py init INV-example`."
                )
            if (
                args.investigation_id
                and args.target
                and args.investigation_id != args.target
            ):
                raise CaseStateError(
                    "The positional investigation ID and --investigation-id disagree."
                )
            cmd_init(workspace, case_id)
            return 0

        if args.command == "cases":
            cmd_cases(workspace)
            return 0

        tasks = discover_tasks()
        if not tasks:
            raise CaseStateError(
                f"No task files found in {REFERENCES}. Check the plugin installation."
            )

        context = select_case(workspace, args.investigation_id)
        state = load_progress(context)
        validate_progress_for_tasks(state, tasks)

        if args.command == "next":
            cmd_next(tasks, state, context)
        elif args.command == "done":
            if not cmd_done(tasks, state, context, args.evidence_manifest):
                return 2
        elif args.command == "status":
            print_status(tasks, state, context)
        elif args.command == "reset":
            cmd_reset(state, context, force=args.force)
        elif args.command == "jump":
            if not args.target:
                raise CaseStateError("Usage: task_runner.py jump t6.2")
            if not cmd_jump(tasks, state, context, args.target):
                return 2
        elif args.command == "peek":
            if not args.target:
                raise CaseStateError("Usage: task_runner.py peek t9.1")
            cmd_peek(tasks, state, context, args.target)
        elif args.command == "list":
            cmd_list(tasks)
        elif args.command == "notebook":
            cmd_notebook(context)
        elif args.command == "requirements":
            cmd_requirements(tasks, state, args.target, args.out)
        return 0
    except CaseStateError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
