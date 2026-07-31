"""Dependency management — wraps pip for optional module groups."""

import re
import subprocess
import sys

from rich.console import Console
from rich.table import Table

console = Console()

MODULES: dict[str, dict] = {
    "identity": {
        "desc": "Username enumeration and identity research",
        "packages": ["sherlock-project", "maigret"],
    },
    "social": {
        "desc": "Social media archiving and content capture",
        "packages": ["yt-dlp", "gallery-dl", "instaloader", "playwright"],
    },
    "network": {
        "desc": "DNS, domain, and infrastructure investigation",
        "packages": ["dnspython>=2.4", "tldextract>=5.0", "ipwhois>=1.2", "whois>=0.9"],
    },
    "corporate": {
        "desc": "Corporate registry and financial analysis",
        "packages": ["edgartools"],
    },
    "sanctions": {
        "desc": "Sanctions screening and fuzzy matching",
        "packages": ["rapidfuzz>=3.0", "jellyfish>=1.0", "nameparser>=1.1"],
    },
    "geo": {
        "desc": "Geolocation, mapping, and spatial analysis",
        "packages": [
            "geopandas>=0.14",
            "geopy>=2.4",
            "folium>=0.15",
            "pysolar>=0.11",
            "exifread>=3.0",
            "shapely>=2.0",
        ],
    },
    "nlp": {
        "desc": "Natural language processing and entity extraction",
        "packages": ["spacy>=3.7", "nltk>=3.8", "scikit-learn>=1.3"],
    },
    "graph": {
        "desc": "Network graph analysis and visualisation",
        "packages": [
            "networkx>=3.2",
            "scipy>=1.11",
            "pyvis>=0.3",
            "matplotlib>=3.8",
            "plotly>=5.18",
            "seaborn>=0.13",
        ],
    },
    "archiving": {
        "desc": "Evidence preservation and web archiving",
        "packages": ["waybackpy>=3.0", "warcio>=1.7", "trafilatura>=1.6"],
    },
    "documents": {
        "desc": "PDF processing, OCR, and document handling",
        "packages": ["pdfplumber>=0.10", "pypdf>=3.17", "pytesseract>=0.3", "Pillow>=10.0", "markitdown>=0.1"],
    },
    "reporting": {
        "desc": "Report generation (HTML/PDF/Word)",
        "packages": ["jinja2>=3.1", "weasyprint>=60.0", "docxtpl>=0.16", "markdown>=3.5", "wordcloud>=1.9"],
    },
    "entity_resolution": {
        "desc": "Record linkage and entity deduplication",
        "packages": ["recordlinkage>=0.16"],
    },
}
PACKAGE_IMPORTS = {
    "Pillow": "PIL",
    "dnspython": "dns",
    "edgartools": "edgar",
    "scikit-learn": "sklearn",
    "sherlock-project": "sherlock",
}


def import_name(requirement: str) -> str:
    """Return the importable module name for a package requirement."""
    package = re.split(r"[<>=!~]", requirement, maxsplit=1)[0]
    return PACKAGE_IMPORTS.get(package, package.replace("-", "_"))


def list_modules() -> None:
    table = Table(title="ospo dependency modules", show_lines=False, header_style="bold")
    table.add_column("module", style="cyan", no_wrap=True)
    table.add_column("description")
    table.add_column("packages", style="dim")
    for name, meta in MODULES.items():
        table.add_row(name, meta["desc"], str(len(meta["packages"])))
    console.print(table)


def install(modules: list[str]) -> bool:
    unknown = [m for m in modules if m not in MODULES]
    if unknown:
        console.print(f"[red]Unknown modules: {', '.join(unknown)}[/red]")
        console.print(f"Available: {', '.join(MODULES)}")
        return False

    packages = [p for m in modules for p in MODULES[m]["packages"]]
    console.print(f"\nInstalling {len(packages)} packages across {len(modules)} module(s)...\n")

    failed = []
    for pkg in packages:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "-q"],
            capture_output=True, text=True,
        )
        status = "[green]ok[/green]" if result.returncode == 0 else "[red]fail[/red]"
        console.print(f"  {status}  {pkg}")
        if result.returncode != 0:
            failed.append(pkg)

    if failed:
        console.print(f"\n[red]Failed:[/red] {', '.join(failed)}")
        return False
    return True


def check() -> None:
    import importlib
    table = Table(title="dependency health", show_lines=False, header_style="bold")
    table.add_column("module", style="cyan")
    table.add_column("status")
    table.add_column("failed packages", style="dim red")

    for name, meta in MODULES.items():
        missing = []
        for pkg in meta["packages"]:
            try:
                importlib.import_module(import_name(pkg))
            except ImportError:
                missing.append(pkg.split(">=")[0])
        if not missing:
            status = "[green]installed[/green]"
        elif len(missing) < len(meta["packages"]):
            status = "[yellow]partial[/yellow]"
        else:
            status = "[dim]not installed[/dim]"
        table.add_row(name, status, ", ".join(missing) if missing else "")
    console.print(table)
