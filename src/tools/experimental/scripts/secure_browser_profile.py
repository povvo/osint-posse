#!/usr/bin/env python3
"""Controlled browser profile workspace.

Creates and checks a separate browser profile directory for case research. It
writes an audit manifest and launch command so browser activity can be kept
separate from personal browsing.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SUPPORTED_BROWSERS = {"edge", "chrome", "firefox"}


class ProfileError(RuntimeError):
    """Raised when profile setup or launch validation fails."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalise_case_id(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in value.strip())
    cleaned = cleaned.strip("._-")
    if not cleaned:
        raise ProfileError("case id must contain at least one safe character")
    return cleaned[:80]


def ensure_child(root: Path, child: Path) -> Path:
    root_resolved = root.resolve()
    child_resolved = child.resolve()
    try:
        child_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ProfileError(f"path escapes workspace: {child}") from exc
    return child_resolved


def quote_cmd(parts: Iterable[str]) -> str:
    if os.name == "nt":
        return subprocess.list2cmdline(list(parts))
    return " ".join(shlex.quote(part) for part in parts)


@dataclass(frozen=True)
class BrowserProfile:
    case_id: str
    browser: str
    workspace: str
    profile_dir: str
    downloads_dir: str
    captures_dir: str
    notes_dir: str
    logs_dir: str
    executable: str | None
    launch_command: list[str]
    created_at_utc: str
    homepage_urls: list[str]

    @property
    def manifest_path(self) -> Path:
        return Path(self.workspace) / "profile_manifest.json"


def browser_candidates(browser: str) -> list[Path]:
    system = platform.system().lower()
    program_files = [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)")]
    candidates: list[Path] = []
    if system == "windows":
        if browser == "edge":
            candidates += [Path(p) / "Microsoft/Edge/Application/msedge.exe" for p in program_files if p]
        elif browser == "chrome":
            candidates += [Path(p) / "Google/Chrome/Application/chrome.exe" for p in program_files if p]
        elif browser == "firefox":
            candidates += [Path(p) / "Mozilla Firefox/firefox.exe" for p in program_files if p]
    elif system == "darwin":
        app_map = {
            "edge": "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
        }
        candidates.append(Path(app_map[browser]))
    else:
        names = {"edge": "microsoft-edge", "chrome": "google-chrome", "firefox": "firefox"}
        path_env = os.environ.get("PATH", "")
        for folder in path_env.split(os.pathsep):
            candidates.append(Path(folder) / names[browser])
    return candidates


def find_browser(browser: str, explicit: str | None = None) -> Path | None:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.exists():
            raise ProfileError(f"browser executable not found: {path}")
        return path
    for candidate in browser_candidates(browser):
        if candidate.exists():
            return candidate
    return None


def build_launch_command(browser: str, executable: Path | None, profile_dir: Path, downloads_dir: Path, urls: list[str]) -> list[str]:
    exe = str(executable) if executable else browser
    if browser in {"edge", "chrome"}:
        command = [
            exe,
            f"--user-data-dir={profile_dir}",
            "--profile-directory=Default",
            "--no-first-run",
            "--disable-sync",
            "--disable-extensions",
            "--disable-background-networking",
            f"--download-default-directory={downloads_dir}",
        ]
    elif browser == "firefox":
        command = [exe, "-profile", str(profile_dir), "-no-remote"]
    else:
        raise ProfileError(f"unsupported browser: {browser}")
    command.extend(urls)
    return command


def create_profile(case_id: str, browser: str, root: Path, urls: list[str], executable: str | None = None) -> BrowserProfile:
    if browser not in SUPPORTED_BROWSERS:
        raise ProfileError(f"browser must be one of: {', '.join(sorted(SUPPORTED_BROWSERS))}")
    case_id = normalise_case_id(case_id)
    workspace = (root.expanduser() / case_id).resolve()
    profile_dir = ensure_child(workspace, workspace / "profile")
    downloads_dir = ensure_child(workspace, workspace / "downloads")
    captures_dir = ensure_child(workspace, workspace / "captures")
    notes_dir = ensure_child(workspace, workspace / "notes")
    logs_dir = ensure_child(workspace, workspace / "logs")
    for folder in (profile_dir, downloads_dir, captures_dir, notes_dir, logs_dir):
        folder.mkdir(parents=True, exist_ok=True)
    exe = find_browser(browser, executable)
    command = build_launch_command(browser, exe, profile_dir, downloads_dir, urls)
    profile = BrowserProfile(case_id, browser, str(workspace), str(profile_dir), str(downloads_dir), str(captures_dir), str(notes_dir), str(logs_dir), str(exe) if exe else None, command, utc_now(), urls)
    profile.manifest_path.write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")
    write_launch_files(profile)
    return profile


def write_launch_files(profile: BrowserProfile) -> None:
    workspace = Path(profile.workspace)
    command = quote_cmd(profile.launch_command)
    if os.name == "nt":
        launch_file = workspace / "launch_profile.cmd"
        launch_file.write_text(f"@echo off\r\n{command}\r\n", encoding="utf-8")
    else:
        launch_file = workspace / "launch_profile.sh"
        launch_file.write_text(f"#!/usr/bin/env sh\nexec {command}\n", encoding="utf-8")
        launch_file.chmod(0o755)
    notes = Path(profile.notes_dir) / "README.md"
    if not notes.exists():
        notes.write_text(
            "# Research profile notes\n\n"
            "Record query terms, source URLs, decisions, negative results, and follow-up actions here.\n",
            encoding="utf-8",
        )


def load_manifest(workspace: Path) -> dict:
    manifest = workspace / "profile_manifest.json"
    if not manifest.exists():
        raise ProfileError(f"manifest not found: {manifest}")
    return json.loads(manifest.read_text(encoding="utf-8"))


def inspect_profile(workspace: Path) -> dict:
    manifest = load_manifest(workspace)
    required = ["profile_dir", "downloads_dir", "captures_dir", "notes_dir", "logs_dir"]
    checks = []
    for key in required:
        path = Path(manifest[key])
        checks.append({"key": key, "path": str(path), "exists": path.exists(), "is_dir": path.is_dir()})
    launch_name = "launch_profile.cmd" if os.name == "nt" else "launch_profile.sh"
    launch_path = workspace / launch_name
    checks.append({"key": "launch_file", "path": str(launch_path), "exists": launch_path.exists(), "is_file": launch_path.is_file()})
    return {
        "workspace": str(workspace),
        "case_id": manifest.get("case_id"),
        "browser": manifest.get("browser"),
        "manifest_exists": True,
        "checks": checks,
        "ready": all(item.get("exists") for item in checks),
    }


def launch_profile(workspace: Path, execute: bool = False) -> dict:
    manifest = load_manifest(workspace)
    command = manifest["launch_command"]
    if execute:
        subprocess.Popen(command, cwd=str(workspace))
    return {"workspace": str(workspace), "execute": execute, "command": command, "command_text": quote_cmd(command)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and inspect a separate browser profile workspace.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create or update a profile workspace")
    init.add_argument("--case-id", required=True)
    init.add_argument("--browser", choices=sorted(SUPPORTED_BROWSERS), default="edge")
    init.add_argument("--root", default=str(Path.cwd() / "browser_profiles"))
    init.add_argument("--url", action="append", default=[])
    init.add_argument("--executable")

    inspect = sub.add_parser("inspect", help="Inspect an existing workspace")
    inspect.add_argument("workspace")

    launch = sub.add_parser("command", help="Print the browser command for a workspace")
    launch.add_argument("workspace")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            profile = create_profile(args.case_id, args.browser, Path(args.root), args.url, args.executable)
            print(json.dumps(asdict(profile), indent=2))
        elif args.command == "inspect":
            print(json.dumps(inspect_profile(Path(args.workspace)), indent=2))
        else:
            print(json.dumps(launch_profile(Path(args.workspace), False), indent=2))
    except ProfileError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
