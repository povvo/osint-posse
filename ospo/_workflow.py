"""Canonical installed workflow, tool, template, setup, and doctor command layer."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from importlib import metadata
from pathlib import Path

from . import __version__
from ._paths import release_resources


TOOLS = {
    "blockchain-intel": "blockchain_intel.py",
    "chronology": "chronological_matrix.py",
    "content-archiver": "content_archiver.py",
    "corporate-intel": "corporate_intel.py",
    "document-intel": "document_intel.py",
    "domain-intel": "domain_intel.py",
    "email-intel": "email_intel.py",
    "entity-resolver": "entity_resolver.py",
    "evidence-preservation": "evidence_preservation.py",
    "financial-analysis": "financial_analysis.py",
    "geolocation": "geolocation.py",
    "geospatial-context": "geospatial_context.py",
    "media-verification": "media_verification.py",
    "network-graph": "network_graph.py",
    "news-monitor": "news_monitor.py",
    "phone-intel": "phone_intel.py",
    "public-records": "public_records.py",
    "report-generator": "report_generator.py",
    "sanctions-screen": "sanctions_screen.py",
    "search-intel": "search_intel.py",
    "source-grader": "source_grader.py",
    "source-registry": "source_registry.py",
    "threat-reputation": "threat_reputation.py",
    "username-enum": "username_enum.py",
    "web-archive": "web_archive_intel.py",
}

WORKFLOW_ACTIONS = (
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
)


def _scripts() -> Path:
    return release_resources().skill / "scripts"


def _run(script: str, arguments: list[str]) -> int:
    return subprocess.run([sys.executable, str(_scripts() / script), *arguments], check=False).returncode


def doctor() -> int:
    resources = release_resources()
    task_count = len(list((resources.skill / "references").rglob("t*.md")))
    template_count = len(list((resources.skill / "templates").rglob("*.md")))
    missing = [
        dependency
        for dependency in ("requests", "rich", "typer")
        if importlib.util.find_spec(dependency) is None
    ]
    try:
        installed = metadata.version("osint-posse")
    except metadata.PackageNotFoundError:
        installed = None
    print(f"osint-posse {installed or __version__}")
    print(f"Resources: {task_count} task cards, {template_count} templates")
    if missing:
        print("Missing core dependencies: " + ", ".join(missing), file=sys.stderr)
        return 2
    print("Core runtime and packaged resources are ready.")
    return 0


def build_parser(prog: str = "green-ink") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Governed investigation workflow and bundled OSINT tools.",
    )
    parser.add_argument("--version", action="version", version=f"{prog} {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    workflow = commands.add_parser(
        "workflow",
        help="Run the governed 56-task investigation workflow.",
    )
    workflow.add_argument("action", choices=WORKFLOW_ACTIONS)
    workflow.add_argument("arguments", nargs=argparse.REMAINDER)
    template = commands.add_parser(
        "template",
        help="Discover or render a bundled template.",
    )
    template.add_argument("action", choices=("list", "render"))
    template.add_argument("arguments", nargs=argparse.REMAINDER)
    tool = commands.add_parser("tool")
    tool_commands = tool.add_subparsers(dest="tool_command", required=True)
    tool_commands.add_parser("list")
    run = tool_commands.add_parser("run")
    run.add_argument("name", choices=sorted(TOOLS))
    run.add_argument("--standalone", action="store_true")
    run.add_argument("arguments", nargs=argparse.REMAINDER)
    setup = commands.add_parser("setup")
    setup.add_argument("arguments", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None, *, prog: str = "green-ink") -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)
    if args.command == "doctor":
        return doctor()
    if args.command == "workflow":
        return _run("task_runner.py", [args.action, *args.arguments])
    if args.command == "template":
        template_arguments = ["--list"] if args.action == "list" else args.arguments
        return _run("template_builder.py", template_arguments)
    if args.command == "setup":
        return _run("setup.py", args.arguments)
    if args.command == "tool" and args.tool_command == "list":
        for name, filename in sorted(TOOLS.items()):
            marker = "ok" if (_scripts() / filename).is_file() else "missing"
            print(f"{name:<24} {marker}")
        return 0
    if args.command == "tool" and args.tool_command == "run":
        if not args.standalone:
            parser.error("tool run requires --standalone")
        arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
        return _run(TOOLS[args.name], arguments)
    parser.error("unsupported command")
    return 2
