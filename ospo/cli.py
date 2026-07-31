"""The canonical ``ospo`` command surface."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from . import __version__, _workflow
from . import _deps as deps
from ._install import InstallConflict, install_release, uninstall_release

console = Console()
app = typer.Typer(
    name="ospo",
    help="Governed OSINT workflow, release resources, and bounded standalone tools.",
    add_completion=False,
    no_args_is_help=True,
)
tool_app = typer.Typer(help="List or run bundled tools.", no_args_is_help=True)
deps_app = typer.Typer(help="Inspect or install optional dependency groups.", no_args_is_help=True)
app.add_typer(tool_app, name="tool")
app.add_typer(deps_app, name="deps")


def _scope(value: str) -> str:
    if value not in {"project", "user"}:
        raise typer.BadParameter("must be 'project' or 'user'")
    return value


def _show_result(result) -> None:
    label = "would change" if result.dry_run else "changed"
    console.print(
        f"{result.action}: {len(result.copied) + len(result.removed)} {label}; "
        f"{len(result.unchanged)} unchanged; {len(result.preserved)} preserved"
    )


@app.command()
def install(
    claude: Annotated[bool, typer.Option("--claude", help="Include Claude agent definitions.")] = False,
    codex: Annotated[bool, typer.Option("--codex", help="Include Codex agent definitions.")] = False,
    scope: Annotated[
        str,
        typer.Option("--scope", callback=_scope, help="Install to project or user scope."),
    ] = "project",
    root: Annotated[Path | None, typer.Option("--root", help="Explicit scope root.")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Preflight without writing.")] = False,
) -> None:
    """Install the skill and selected agents after collision preflight."""
    try:
        _show_result(
            install_release(
                scope=scope,
                root=root,
                claude=claude,
                codex=codex,
                dry_run=dry_run,
            )
        )
    except InstallConflict as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(2) from exc


@app.command()
def uninstall(
    claude: Annotated[bool, typer.Option("--claude", help="Include owned Claude agent files.")] = False,
    codex: Annotated[bool, typer.Option("--codex", help="Include owned Codex agent files.")] = False,
    scope: Annotated[str, typer.Option("--scope", callback=_scope)] = "project",
    root: Annotated[Path | None, typer.Option("--root")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Remove only unchanged files recorded in ospo's ownership ledger."""
    try:
        _show_result(
            uninstall_release(
                scope=scope,
                root=root,
                claude=claude,
                codex=codex,
                dry_run=dry_run,
            )
        )
    except InstallConflict as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(2) from exc


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
        "help_option_names": [],
    }
)
def workflow(ctx: typer.Context) -> None:
    """Run the evidence-gated 56-task workflow."""
    raise typer.Exit(_workflow.main(["workflow", *ctx.args], prog="ospo"))


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
        "help_option_names": [],
    }
)
def template(ctx: typer.Context) -> None:
    """Discover or render a bundled workflow template."""
    raise typer.Exit(_workflow.main(["template", *ctx.args], prog="ospo"))


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
        "help_option_names": [],
    }
)
def setup(ctx: typer.Context) -> None:
    """Inspect or install workflow dependency groups."""
    raise typer.Exit(_workflow.main(["setup", *ctx.args], prog="ospo"))


@app.command()
def doctor() -> None:
    """Check the installed version, resources, and core dependencies."""
    raise typer.Exit(_workflow.doctor())


@tool_app.command("list")
def tool_list() -> None:
    """List the allow-listed bundled tools."""
    raise typer.Exit(_workflow.main(["tool", "list"], prog="ospo"))


@tool_app.command(
    "run",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def tool_run(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Allow-listed tool name.")],
    standalone: Annotated[bool, typer.Option("--standalone", help="Confirm no workflow-state mutation.")] = False,
) -> None:
    """Run one tool without changing workflow state."""
    arguments = ["tool", "run", name]
    if standalone:
        arguments.append("--standalone")
    arguments.extend(["--", *ctx.args])
    raise typer.Exit(_workflow.main(arguments, prog="ospo"))


@deps_app.command("list")
def deps_list() -> None:
    """List optional dependency groups."""
    deps.list_modules()


@deps_app.command("check")
def deps_check() -> None:
    """Check installed optional dependencies."""
    deps.check()


@deps_app.command("install")
def deps_install(
    modules: Annotated[str, typer.Argument(help="Comma-separated groups or 'all'.")],
) -> None:
    """Install optional dependency groups."""
    selected = list(deps.MODULES) if modules == "all" else [item.strip() for item in modules.split(",")]
    if not deps.install(selected):
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Print the runtime version."""
    console.print(__version__)


if __name__ == "__main__":
    app()
