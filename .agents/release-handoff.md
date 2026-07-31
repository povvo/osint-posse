# Release Handoff

Repository: `https://github.com/povvo/osint-posse`

Target branch: `main`

Version: `0.1.0`

Tag: not created

Package publication: not performed

## Delivered candidate

The repository is prepared as one reviewed root commit containing the complete
public release candidate. The pre-work source tree remains recoverable from the
verified archive recorded in `.agents/audit.md`.

The supported Python distribution contains Recon Rodeo, 60 Claude agents, 60
Codex agents, 56 task cards, 21 templates, the `ospo` CLI, and the `green-ink`
compatibility entry point. The repository additionally contains three
dependency-locked Worker sources. `ospo-db` is the recommended persistent
investigation database; Green Ink remains the workflow CLI.

## Verification contract

Required local and CI evidence:

- package and Recon Rodeo unit suites;
- Ruff and mypy;
- Python 3.10–3.14 clean installs;
- all supported tool-module `--help` imports;
- source inventory and prohibited-file verification;
- sdist build followed by wheel build from that sdist;
- distribution inventory and clean-installed CLI smoke tests;
- locked Worker installs, runtime audits, tests/type checks, and builds;
- Gitleaks against the complete single-commit history.

Required remote evidence:

- exactly one commit on `main`;
- green required checks at that commit;
- secret scanning, push protection, Dependabot alerts and fixes, and code
  scanning enabled;
- protected `main` with linear history, conversation resolution, required
  checks, and force-push/deletion prevention;
- inherited Povvo community-health files and project-specific safety documents
  visible from the public repository.

## Rollback

Before publication, replace the candidate from the verified local tree or
restore the pre-work archive. After publication, never move or replace the
`v0.1.0` tag. Repair on a new commit and issue a corrective version, preserving
the original release evidence and documenting impact.

## Publication boundary

This handoff authorises repository finalisation only. It does not authorise a
tag, GitHub Release, Cloudflare deployment, or PyPI publication. Those actions
require explicit maintainer approval after final CI and environment readback.
