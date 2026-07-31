#!/usr/bin/env python3
"""Installed command surface for Green Ink's workflow and bundled OSINT tools."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
sys.path.insert(0, str(SCRIPT_DIR))
from resource_paths import resource_directories


try:
    VERSION = metadata.version("osint-posse")
except metadata.PackageNotFoundError:
    VERSION = "0.1.0"

TOOLS = {
    "blockchain-intel": ("scripts.blockchain_intel", "Inspect public blockchain identifiers."),
    "chronology": ("scripts.chronological_matrix", "Validate and analyse chronological event data."),
    "content-archiver": ("scripts.content_archiver", "Archive supported public content."),
    "corporate-intel": ("scripts.corporate_intel", "Collect public corporate intelligence."),
    "document-intel": ("scripts.document_intel", "Inspect local investigation documents."),
    "domain-intel": ("scripts.domain_intel", "Collect public domain and DNS intelligence."),
    "email-intel": ("scripts.email_intel", "Inspect public signals for an email address."),
    "entity-resolver": ("scripts.entity_resolver", "Resolve candidate entity records."),
    "evidence-preservation": ("scripts.evidence_preservation", "Capture and hash public web evidence."),
    "financial-analysis": ("scripts.financial_analysis", "Analyse supplied financial data."),
    "geolocation": ("scripts.geolocation", "Evaluate geolocation evidence."),
    "geospatial-context": ("scripts.geospatial_context", "Collect geospatial context."),
    "media-verification": ("scripts.media_verification", "Inspect supplied media evidence."),
    "network-graph": ("scripts.network_graph", "Build and analyse an evidence-backed network graph."),
    "news-monitor": ("scripts.news_monitor", "Query public news sources."),
    "phone-intel": ("scripts.phone_intel", "Inspect public signals for a phone number."),
    "public-records": ("scripts.public_records", "Query supported public-record sources."),
    "report-generator": ("scripts.report_generator", "Validate and render an analytical report."),
    "sanctions-screen": ("scripts.sanctions_screen", "Screen entities against public sanctions data."),
    "search-intel": ("scripts.search_intel", "Run supported public search collection."),
    "source-grader": ("scripts.source_grader", "Grade a source using the Admiralty system."),
    "source-registry": ("scripts.source_registry", "Manage a local source register."),
    "threat-reputation": ("scripts.threat_reputation", "Check public threat-reputation sources."),
    "username-enum": ("scripts.username_enum", "Enumerate public username occurrences."),
    "web-archive": ("scripts.web_archive_intel", "Query Wayback and Common Crawl indexes."),
}

DEPENDENCIES = {
    "requests": ("requests", "core", "required"),
    "httpx": ("httpx", "core", "required"),
    "aiohttp": ("aiohttp", "core", "required"),
    "beautifulsoup4": ("bs4", "core", "required"),
    "lxml": ("lxml", "core", "required"),
    "pandas": ("pandas", "core", "required"),
    "numpy": ("numpy", "core", "required"),
    "rich": ("rich", "core", "required"),
    "tqdm": ("tqdm", "core", "required"),
    "python-dateutil": ("dateutil", "core", "required"),
    "pytz": ("pytz", "core", "required"),
    "networkx": ("networkx", "graph", "workflow_required"),
    "scipy": ("scipy", "graph", "workflow_required"),
    "sherlock-project": ("sherlock_project", "identity", "optional"),
    "maigret": ("maigret", "identity", "optional"),
    "yt-dlp": ("yt_dlp", "social", "optional"),
    "gallery-dl": ("gallery_dl", "social", "optional"),
    "instaloader": ("instaloader", "social", "optional"),
    "playwright": ("playwright", "social", "optional"),
    "dnspython": ("dns", "network", "optional"),
    "tldextract": ("tldextract", "network", "optional"),
    "ipwhois": ("ipwhois", "network", "optional"),
    "whois": ("whois", "network", "optional"),
    "edgartools": ("edgar", "corporate", "optional"),
    "rapidfuzz": ("rapidfuzz", "sanctions", "optional"),
    "jellyfish": ("jellyfish", "sanctions", "optional"),
    "nameparser": ("nameparser", "sanctions", "optional"),
    "geopandas": ("geopandas", "geo", "optional"),
    "geopy": ("geopy", "geo", "optional"),
    "folium": ("folium", "geo", "optional"),
    "pysolar": ("pysolar", "geo", "optional"),
    "exifread": ("exifread", "geo", "optional"),
    "shapely": ("shapely", "geo", "optional"),
    "spacy": ("spacy", "nlp", "optional"),
    "nltk": ("nltk", "nlp", "optional"),
    "scikit-learn": ("sklearn", "nlp", "optional"),
    "pyvis": ("pyvis", "graph", "optional"),
    "matplotlib": ("matplotlib", "graph", "optional"),
    "plotly": ("plotly", "graph", "optional"),
    "seaborn": ("seaborn", "graph", "optional"),
    "waybackpy": ("waybackpy", "archiving", "optional"),
    "warcio": ("warcio", "archiving", "optional"),
    "trafilatura": ("trafilatura", "archiving", "optional"),
    "pdfplumber": ("pdfplumber", "documents", "optional"),
    "pypdf": ("pypdf", "documents", "optional"),
    "pytesseract": ("pytesseract", "documents", "optional"),
    "Pillow": ("PIL", "documents", "optional"),
    "markitdown": ("markitdown", "documents", "optional"),
    "jinja2": ("jinja2", "reporting", "optional"),
    "weasyprint": ("weasyprint", "reporting", "optional"),
    "docxtpl": ("docxtpl", "reporting", "optional"),
    "markdown": ("markdown", "reporting", "optional"),
    "wordcloud": ("wordcloud", "reporting", "optional"),
    "recordlinkage": ("recordlinkage", "entity_resolution", "optional"),
}


class CliUsageError(RuntimeError):
    """Raised for bounded, machine-readable command-line usage errors."""


class GreenInkArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


def _emit_json(ok: bool, command: str, data: dict | None = None, *, code: str = "", message: str = "") -> None:
    payload = {"ok": ok, "command": command}
    if ok:
        payload["data"] = data or {}
    else:
        payload["error"] = {"code": code, "message": message}
    print(json.dumps(payload, sort_keys=True))


def _module_path(module_name: str) -> Path:
    spec = importlib.util.find_spec(module_name)
    if spec is None or not spec.origin:
        raise RuntimeError(f"Installed runtime module is missing: {module_name}")
    path = Path(spec.origin).resolve()
    if not path.is_file():
        raise RuntimeError(f"Installed runtime module is not a file: {module_name}")
    return path


def _run_module(module_name: str, argv: list[str], json_output: bool, command: str) -> int:
    path = _module_path(module_name)
    completed = subprocess.run(
        [sys.executable, str(path), *argv],
        text=True,
        capture_output=json_output,
        check=False,
    )
    if not json_output:
        return completed.returncode
    if completed.returncode == 0:
        _emit_json(
            True,
            command,
            {"exit_code": 0, "stdout": completed.stdout, "stderr": completed.stderr},
        )
    else:
        message = completed.stderr.strip() or completed.stdout.strip() or "Command failed."
        _emit_json(False, command, code="COMMAND_FAILED", message=message)
    return completed.returncode


def _run_tool(
    name: str,
    argv: list[str],
    json_output: bool,
    receipt: str | None,
) -> int:
    module_name = TOOLS[name][0]
    path = _module_path(module_name)
    completed = subprocess.run(
        [sys.executable, str(path), *argv],
        text=True,
        capture_output=True,
        check=False,
    )
    receipt_path = None
    if receipt:
        receipt_path = Path(receipt).expanduser().resolve()
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "1.0",
            "tool_name": name,
            "module": module_name,
            "arguments": argv,
            "exit_code": completed.returncode,
            "executed_at_utc": datetime.now(timezone.utc).isoformat(),
            "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
            "workflow_progress_accessed": False,
        }
        receipt_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    if json_output:
        if completed.returncode == 0:
            _emit_json(
                True,
                f"tool run {name}",
                {
                    "exit_code": 0,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                    "receipt": str(receipt_path) if receipt_path else None,
                },
            )
        else:
            message = completed.stderr.strip() or completed.stdout.strip() or "Tool failed."
            _emit_json(False, f"tool run {name}", code="TOOL_FAILED", message=message)
    else:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        if receipt_path:
            print(f"Receipt: {receipt_path}", file=sys.stderr)
    return completed.returncode


def doctor(json_output: bool) -> int:
    references, templates = resource_directories()
    dependency_status = {}
    for name, (module_name, group, level) in DEPENDENCIES.items():
        available = importlib.util.find_spec(module_name) is not None
        dependency_status[name] = {
            "available": available,
            "group": group,
            "level": level,
        }

    resources = {
        "references_available": references.is_dir(),
        "reference_files": len(list(references.rglob("*.md"))) if references.is_dir() else 0,
        "templates_available": templates.is_dir(),
        "template_files": len(list(templates.rglob("*.md"))) if templates.is_dir() else 0,
    }
    missing_required = [
        name
        for name, status in dependency_status.items()
        if status["level"] == "required" and not status["available"]
    ]
    missing_workflow = [
        name
        for name, status in dependency_status.items()
        if status["level"] == "workflow_required" and not status["available"]
    ]
    missing_optional = [
        name
        for name, status in dependency_status.items()
        if status["level"] == "optional" and not status["available"]
    ]
    resources_ready = all(
        (resources["references_available"], resources["templates_available"])
    )
    runtime_ready = resources_ready and not missing_required
    workflow_ready = runtime_ready and not missing_workflow
    try:
        installed_version = metadata.version("osint-posse")
    except metadata.PackageNotFoundError:
        installed_version = None
    data = {
        "version": installed_version or VERSION,
        "installed_distribution": installed_version is not None,
        "python": sys.version.split()[0],
        "interpreter": sys.executable,
        "dependencies": dependency_status,
        "resources": resources,
        "ready": runtime_ready,
        "workflow_ready": workflow_ready,
        "missing_required": missing_required,
        "missing_workflow_required": missing_workflow,
        "missing_optional": missing_optional,
        "setup": {
            "required": None if runtime_ready else f'"{sys.executable}" -m pip install osint-posse',
            "workflow": None if workflow_ready else f'"{sys.executable}" -m pip install "osint-posse[graph]"',
            "all": f'"{sys.executable}" -m pip install "osint-posse[all]"',
        },
        "auth_required": False,
    }
    if json_output:
        _emit_json(True, "doctor", data)
    else:
        print(f"Green Ink {data['version']}")
        print(f"Python: {data['python']} ({data['interpreter']})")
        print(f"Resources: {resources['reference_files']} task/reference files, {resources['template_files']} templates")
        for name, status in dependency_status.items():
            marker = "ok" if status["available"] else "missing"
            print(f"  {name:<18} {marker:<7} ({status['group']}, {status['level']})")
        if missing_required:
            print("Required runtime incomplete: " + ", ".join(missing_required), file=sys.stderr)
            print("Install with: " + data["setup"]["required"], file=sys.stderr)
        if missing_workflow:
            print("Mandatory graph route incomplete: " + ", ".join(missing_workflow), file=sys.stderr)
            print("Install with: " + data["setup"]["workflow"], file=sys.stderr)
        if workflow_ready:
            print("Core runtime and mandatory workflow route ready.")
        if missing_optional:
            print("Optional packages missing: " + ", ".join(missing_optional))
    return 0 if workflow_ready else 2


def tool_list(json_output: bool) -> int:
    items = [
        {"name": name, "description": description, "available": importlib.util.find_spec(module) is not None}
        for name, (module, description) in sorted(TOOLS.items())
    ]
    if json_output:
        _emit_json(True, "tool list", {"tools": items})
    else:
        for item in items:
            marker = "ok" if item["available"] else "missing"
            print(f"{item['name']:<24} {marker:<7} {item['description']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = GreenInkArgumentParser(
        prog="green-ink",
        description="Green Ink investigation workflow and standalone OSINT command layer.",
        epilog=(
            "Use workflow for governed case progression. Use `tool run --standalone` "
            "for a single allow-listed OSINT utility without reading or changing case progress."
        ),
    )
    parser.add_argument("--version", action="version", version=f"green-ink {VERSION}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("doctor", help="Check installed resources and mandatory dependencies.")

    workflow = subcommands.add_parser("workflow", help="Run the governed 56-task investigation workflow.")
    workflow.add_argument(
        "action",
        choices=["init", "cases", "next", "done", "status", "reset", "jump", "peek", "list", "notebook", "requirements"],
    )
    workflow.add_argument("arguments", nargs=argparse.REMAINDER)

    template = subcommands.add_parser("template", help="Discover or render bundled templates.")
    template.add_argument("action", choices=["list", "render"])
    template.add_argument("arguments", nargs=argparse.REMAINDER)

    tool = subcommands.add_parser("tool", help="Discover and run allow-listed bundled OSINT tools.")
    tool_commands = tool.add_subparsers(dest="tool_command", required=True)
    tool_commands.add_parser("list", help="List runnable bundled OSINT tools.")
    run = tool_commands.add_parser("run", help="Run one bundled tool outside workflow progression.")
    run.add_argument("name", choices=sorted(TOOLS))
    run.add_argument("--standalone", action="store_true", help="Confirm this run is isolated from workflow state.")
    run.add_argument("--receipt", help="Write a workflow-neutral execution receipt to this user path.")

    setup = subcommands.add_parser("setup", help="Install or inspect Green Ink dependency groups.")
    setup.add_argument("arguments", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    json_output = False
    while "--json" in raw:
        raw.remove("--json")
        json_output = True
    parser = build_parser()
    try:
        args, unknown = parser.parse_known_args(raw)
        is_tool_run = args.command == "tool" and args.tool_command == "run"
        if unknown and not is_tool_run and args.command != "setup":
            parser.error("unrecognized arguments: " + " ".join(unknown))
        if args.command == "doctor":
            return doctor(json_output)
        if args.command == "workflow":
            return _run_module(
                "scripts.task_runner",
                [args.action, *args.arguments],
                json_output,
                f"workflow {args.action}",
            )
        if args.command == "template":
            template_args = ["--list"] if args.action == "list" else args.arguments
            return _run_module(
                "scripts.template_builder", template_args, json_output, f"template {args.action}"
            )
        if args.command == "tool" and args.tool_command == "list":
            return tool_list(json_output)
        if args.command == "tool" and args.tool_command == "run":
            if not args.standalone:
                message = "tool run requires --standalone; workflow progress is never implicit."
                if json_output:
                    _emit_json(False, "tool run", code="STANDALONE_REQUIRED", message=message)
                else:
                    print(f"Error: {message}", file=sys.stderr)
                return 2
            tool_args = list(unknown)
            if tool_args[:1] == ["--"]:
                tool_args = tool_args[1:]
            return _run_tool(args.name, tool_args, json_output, args.receipt)
        if args.command == "setup":
            setup_args = raw[raw.index("setup") + 1 :]
            if setup_args[:1] == ["--"]:
                setup_args = setup_args[1:]
            return _run_module("scripts.setup", setup_args, json_output, "setup")
        raise RuntimeError("Unsupported command.")
    except CliUsageError as exc:
        if json_output:
            _emit_json(False, "green-ink", code="USAGE_ERROR", message=str(exc))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        if json_output:
            _emit_json(False, "green-ink", code="RUNTIME_ERROR", message=str(exc))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
