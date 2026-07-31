# OSINT Posse

OSINT Posse packages Recon Rodeo: a local-first investigation workflow with six
phases, 56 evidence-gated tasks, and optional agent definitions for Claude and
Codex. It helps an operator record scope, sources, decisions, task evidence, and
analytical uncertainty. It does not establish legal authority, investigative
correctness, or a chain of custody by becoming installable. Wheels have tried
less ambitious forms of jurisprudence.

Status: pre-release. The first intended release is `0.1.0`. No PyPI package,
GitHub release, or support response window is claimed yet.

## What is included

- The `recon-rodeo` skill, task cards, templates, and bounded scripts.
- 60 Claude agent definitions and 60 Codex agent definitions.
- The `ospo` CLI for installation, workflow progression, templates, tools,
  dependency setup, and diagnostics.
- The `green-ink` compatibility alias for the governed workflow command layer.

Experimental scripts and Cloudflare Worker sources are present in the source
tree but are not part of the supported `0.1.0` runtime contract.

## Build and install this pre-release

Until a release is published, build from a reviewed source tree:

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
ospo tool run NAME --standalone -- ...
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
admissibility. See [Evidence and provenance](docs/evidence-and-provenance.md).

Raw research PDFs and exports are excluded from release staging until each item
has a complete, positive redistribution decision in
[the provenance ledger](docs/research/provenance.csv). Citations and original
synthesis may remain public without smuggling the source archive into the first
commit under a large coat.

## Responsible use

Use the workflow only with recorded authority, a defined purpose, minimised
collection, and a named accountable operator. Psychological profiling is off by
default and is not required for the normal workflow. OSINT Posse must not be
used for automated high-impact decisions or prohibited targeting.

Read:

- [Responsible use](docs/responsible-use.md)
- [Privacy and data handling](docs/privacy-and-data-handling.md)
- [Security model](docs/security-model.md)

These documents describe operator duties and product boundaries. They are not
runtime enforcement and do not replace legal, safeguarding, or evidentiary
review.

## Support boundary

The first release will support only local package and workflow behaviour covered
by release fixtures. Live external services, experimental scripts, Cloudflare
deployment, third-party terms, legal conclusions, and unclassified research
artefacts are outside that claim. Owner-level contributing, security, support,
funding, issue, and pull-request files are intended to be inherited when the
repository is created; their presence must be verified then.

## Release checks

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s src/skills/recon-rodeo/scripts -p 'test_*.py' -v
python3 scripts/verify_release.py --source .
python3 -m build --sdist
python3 -m pip wheel --no-deps --wheel-dir dist dist/*.tar.gz
python3 scripts/verify_release.py --dist dist
```

The release process, artefact inventory, and remote gates are documented in
[Release process](docs/release-process.md).

## Licence

[MIT](LICENSE).
