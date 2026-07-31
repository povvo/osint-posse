# Changelog

Notable changes are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- A self-contained distribution containing Recon Rodeo and both 60-agent packs.
- Project-scoped, hash-owned installation with preflight and dry-run support.
- One governed `ospo` command surface plus the `green-ink` compatibility alias.
- Release verification, clean-install fixtures, CI, and a gated publishing workflow.
- Reproducible lockfiles, tests, type checks, audits, and build checks for the
  three bundled Cloudflare Workers.
- SHA-256 checksum and GitHub artifact-attestation steps for release
  distributions.
- Responsible-use, privacy, security, evidence, provenance, and release documentation.

### Changed

- Set the working first-release version to `0.1.0`.
- Require an evidence manifest before workflow task completion.
- Describe web capture output as an acquisition receipt, with its proof limits.
- Make sensitive profiling optional, separately approved, and prohibited for
  automated high-impact decisions.
- Define `ospo-db` as the recommended persistent investigation database and
  Green Ink as the workflow CLI with limited local continuity state.

### Fixed

- Updated stale state-schema assertions.
- Aligned quickstart commands with the installed workflow gate.
- Restored release-verifier compatibility with Python 3.10.
- Passed the ephemeral workflow token required by Gitleaks pull-request scans.
- Upgraded the Cloudflare Agents, MCP SDK, Zod, Wrangler peer, and Workers type
  dependency set to remove all known npm audit findings.
- Required authentication for `ospo-db`, completed its progress/evidence
  round-trip contract, made case mutations atomic, and added its CI test
  surface.
- Bound tool receipts to cases and tasks, rejected replay, and archived
  completion manifests with evidence hashes.
- Preserved original HTTP response bytes, blocked private browser requests,
  gated external downloaders, repaired case ZIP export, and removed Python
  3.10-incompatible datetime imports.
- Made installer ownership portable across project moves and recoverable after
  interrupted copies.

The dated `0.1.0` section and comparison links will be added when the release is
actually cut.
