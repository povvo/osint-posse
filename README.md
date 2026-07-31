<p align="center">
  <img src="assets/banner.png" alt="OSINT Posse — structured OSINT investigation framework">
</p>

# OSINT Posse

OSINT Posse is a comprehensive, standardised framework for conducting
open-source intelligence investigations through a structured six-phase
lifecycle. It combines 56 evidence-gated tasks with analytical methods including
Analysis of Competing Hypotheses and the Person, Object, Location, Event data
model. Procedures cover authority and purpose recording, SHA-256 acquisition
receipts, negative-search logging, supervisory review, and the controlled use of
programmatic tools across corporate, geospatial, financial, identity, media, and
technical domains.

The framework serves as both an operating manual for AI-assisted research and a
procedural route from raw public data to transparent, defensible intelligence
products. Its controls record legal and ethical decisions; they do not confer
legal authority, guarantee investigative correctness, or produce a chain of
custody merely because the wheel installed successfully. Packaging has limits,
despite several centuries of administrative optimism.

Current source release: `v0.1.0`. This version defines the supported local
package and workflow contract. Cloudflare deployment, third-party services, and
package-index distribution remain separately operated surfaces.

## What is included

- The `recon-rodeo` skill, task cards, templates, and bounded scripts.
- 60 Claude agent definitions and 60 Codex agent definitions.
- The `ospo` CLI for installation, workflow progression, templates, tools,
  dependency setup, and diagnostics.
- The Green Ink controller CLI, available through the `green-ink` entry point.

Experimental scripts and three dependency-locked Cloudflare Worker sources are
present in the source tree but are not part of the supported `0.1.0` Python
runtime contract. CI checks the applicable Worker surfaces through tests,
audits, and dry-run builds; it does not deploy them. `ospo-db` is the recommended
persistent investigation database: an authenticated 26-tool MCP service backed
by Cloudflare D1. Green Ink is the controller CLI.

## Build and install v0.1.0

Build from a reviewed source tree:

```bash
python3 -m build --sdist
python3 -m pip wheel --no-deps --wheel-dir dist dist/*.tar.gz
python3 -m pip install dist/osint_posse-0.1.0-py3-none-any.whl
ospo doctor
```

`ospo install` defaults to the current project. It will not overwrite an
unowned conflict.

```bash
ospo install --dry-run
ospo install
ospo install --claude --codex
```

Project destinations are `.agents/skills/recon-rodeo`, `.claude/agents`, and
`.codex/agents`. Use `--scope user` only when a user-wide installation is
intended. Every managed file is recorded by SHA-256; uninstall removes only
unchanged files that the ledger says OSINT Posse owns.

```bash
ospo uninstall --dry-run
ospo uninstall
ospo install --scope user --dry-run
```

## First governed task

Run this sequence from a case workspace:

```bash
ospo workflow init INV-example
ospo workflow next
ospo workflow requirements --out evidence-manifest.json
ospo workflow done --evidence-manifest evidence-manifest.json
ospo workflow status
```

The generated manifest is deliberately incomplete. Fill its requirement,
script, template, tool, and notebook evidence before `done`. An incomplete
manifest is rejected; a valid manifest advances exactly one task.

## Command surface

```text
ospo --help
ospo doctor
ospo install [--claude] [--codex] [--scope project|user] [--dry-run]
ospo uninstall [--claude] [--codex] [--scope project|user] [--dry-run]
ospo workflow ...
ospo template ...
ospo tool list
ospo tool run --standalone NAME -- ...
ospo tool run --standalone --receipt receipt.json \
  --investigation-id INV-example --task-id t3.1a NAME -- ...
ospo setup ...
ospo deps list|check|install
green-ink doctor
green-ink workflow ...
```

Standalone tools never advance workflow state implicitly. `tool run` therefore
requires `--standalone`, which is a small flag carrying a useful amount of
administrative honesty.

## Evidence and provenance

`evidence_preservation.py` writes an acquisition receipt. SHA-256 values can
show that local bytes still match the bytes hashed at receipt creation. They do
not prove operator identity, source authenticity, continuous custody, or legal
admissibility. See
[Evidence and provenance](resources/docs/evidence-and-provenance.md).

Raw research PDFs and exports are excluded from release staging until each item
has a complete, positive redistribution decision in
[the provenance ledger](resources/docs/research/provenance.csv). Citations and original
synthesis may remain public without smuggling the source archive into the first
commit under a large coat.

## Responsible use

Use the workflow only with recorded authority, a defined purpose, minimised
collection, and a named accountable operator. Psychological profiling is off by
default and is not required for the normal workflow. OSINT Posse must not be
used for automated high-impact decisions or prohibited targeting.

Read:

- [Responsible use](resources/docs/responsible-use.md)
- [Privacy and data handling](resources/docs/privacy-and-data-handling.md)
- [Security model](resources/docs/security-model.md)

These documents describe operator duties and product boundaries. They are not
runtime enforcement and do not replace legal, safeguarding, or evidentiary
review.

## Support boundary

Version `v0.1.0` supports local package and workflow behaviour covered by
release fixtures. Live external services, experimental scripts, Cloudflare
deployment, third-party terms, legal conclusions, and unclassified research
artefacts are outside that claim. Owner-level contributing, security, support,
funding, issue, and pull-request policies are inherited from the
[Povvo community-health repository](https://github.com/povvo/.github).
Project-specific responsible-use, privacy, provenance, and security documents
supplement those policies.

## Release checks

```bash
PYTHONPATH=src python3 -m unittest discover -s resources/dev/tests -v
python3 -m unittest discover -s resources/dev/tests/recon_rodeo -p 'test_*.py' -v
python3 resources/dev/scripts/verify_release.py --source .
ruff check src/ospo resources/build/ospo_build_backend.py resources/dev/tests resources/dev/scripts
mypy src/ospo
python3 -m build --sdist
python3 -m pip wheel --no-deps --wheel-dir dist dist/*.tar.gz
python3 resources/dev/scripts/verify_release.py --dist dist
```

Each bundled Cloudflare Worker is also installed from its committed lockfile,
audited with `npm audit --omit=dev --audit-level=moderate`, type-checked, and
built with `wrangler deploy --dry-run`.

The release process, artefact inventory, and remote gates are documented in
[Release process](resources/docs/release-process.md).

## Licence

[MIT](LICENSE).
