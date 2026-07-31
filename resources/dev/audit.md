# Release Readiness Audit

Repository: `povvo/osint-posse`

Candidate: `0.1.0`

Audit date: 2026-07-31

Decision: locally release-ready; publication remains a separate maintainer decision

## Product boundary

OSINT Posse is a standardised six-phase OSINT framework comprising 56
evidence-gated tasks, 60 Claude agent definitions, 60 Codex agent definitions,
21 templates, the Green Ink controller CLI, and three reviewed Cloudflare Worker
sources. `ospo-db` is the recommended persistent investigation database: an
authenticated 26-tool MCP service backed by Cloudflare D1.

## Before-work recovery point

- Archive:
  `/home/povvo/projects/pre-release-archive/osint-posse/osint-posse-before-release-work-2026-07-31.zip`
- Entries: 1,090
- Bytes: 21,914,220
- SHA-256:
  `3849e805bd0ecff84a07eca9bddc1fbda4aeffea74746210c43fed9d55ad4a5b`
- Integrity: `unzip -t` passed

The archive deliberately contains the complete pre-release working tree,
including ignored research inputs and transport debris. Those files remain
excluded from the public release tree.

## Remediated release blockers

- Packaged Recon Rodeo and both 60-agent sets into the sdist and wheel.
- Moved the installable Python runtime to `src/ospo`, placed operator
  documentation under `resources/docs`, and isolated tests, audit material,
  release tooling, and the design skill under `resources/dev`.
- Moved the reviewed source-distribution inventory into the in-tree build
  backend and removed `MANIFEST.in` and `uv.lock` from the repository root.
- Excluded all maintainer-only resources and Recon Rodeo test modules from the
  sdist and wheel.
- Made installation collision-preflighted, hash-owned, atomic per file,
  project-move-safe, dry-runnable, and conservative on uninstall.
- Unified the installed `ospo` and `green-ink` workflow/tool command contract.
- Added case-and-task-bound execution receipts, replay rejection, immutable
  completion-manifest retention, and evidence/output hashing.
- Repaired case ZIP export and preserved original HTTP response bytes before
  acquisition hashing and WARC creation.
- Added private-target browser request blocking and explicit opt-in for
  downloader paths that require an egress-restricted environment.
- Restored Python 3.10 compatibility across supported scripts.
- Secured `ospo-db` with fail-closed bearer authentication, bounded request
  bodies, atomic D1 batches, exact database selection, schema migration,
  complete progress/evidence/location round trips, timestamp normalisation,
  relationship integrity checks, and automated tests.
- Locked and gated all three Worker sources in CI and Dependabot.
- Added Ruff, mypy, Python 3.10–3.14, source inventory, sdist-to-wheel,
  clean-install CLI, Worker, dependency audit, and secret-scanning gates.
- Added release tag identity verification, checksums, artifact attestations,
  protected-environment gating, and OIDC PyPI publishing.

## Current local evidence

The final values in this section are regenerated immediately before the single
root commit:

- Package tests: 9 passing.
- Recon Rodeo tests: 13 passing.
- Ruff: passing.
- mypy: passing for seven package source files.
- `ospo-db`: locked install, zero-vulnerability audit, syntax check, and Worker
  tests passing.
- Source release verifier: passing; 682 release-eligible paths with inventory
  SHA-256
  `c2bd9bad652d0e7b41570042b474350e5f36d593036bb60ada3f68213604f3cf`.
- Sdist: 345 members; SHA-256
  `9e98c4b0601eeb026d382f3735c5a133b28244dfb83474060c70a8cac4629d33`.
- Wheel built from that sdist: 263 members; SHA-256
  `2195a40fd19e981cb81515746d72d6096de4b08d64f1561279080bfbb576d28e`.
- Final artefact directory: `/tmp/osint-posse-hook-sdist.iOC8ck`.
- Git diff whitespace check: passing.

The two TypeScript Workers were previously installed, audited with zero known
runtime vulnerabilities, type-checked, and dry-run built. The final GitHub CI
run is authoritative for their clean install after the last source edits.

## Remaining publication gates

The repository candidate may be committed and protected. Do not create
`v0.1.0`, a GitHub Release, or a PyPI publication until the maintainer
explicitly authorises publication. At that point:

1. Confirm all required checks are green at the exact reviewed root commit.
2. Configure and read back the protected `pypi` environment and PyPI trusted
   publisher.
3. Create the protected `v0.1.0` tag at that commit.
4. Run the release workflow without publication and compare artefact hashes.
5. Approve publication separately, then read back PyPI and GitHub release
   surfaces before announcement.
