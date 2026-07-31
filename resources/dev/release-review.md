# Stickler Review

## Executive Verdict

- **Decision:** pass for repository finalisation.
- **Top risk:** first deployment of the recommended `ospo-db` database still
  requires Cloudflare account-level validation, backup policy, and live
  authenticated smoke testing.
- **Confidence:** high for the repository candidate; external deployment and
  publication controls require remote readback.

## Review Scope

- **Inspected:** the Python package, installer, CLI, 56-task workflow, evidence
capture, case management, three Worker sources, D1 schema/setup path,
documentation, CI, release automation, provenance boundary, and current Git
payload.
- **Unavailable:** live Cloudflare, final GitHub ruleset/CI, and PyPI state
because deployment and publication were not authorised.
- **Assumptions:** the repository is being finalised as a release candidate;
tagging, Worker deployment, and package publication are separate decisions.

## Coverage Ledger

- **Files or artefacts fully inspected:** supported Python package and tests,
workflow state and
  completion gates, `ospo-db`, CI/release workflows, dependency manifests,
  release verifier, README and release documentation.
- **Files or artefacts partially inspected:** the 267 explicitly experimental
scripts outside the
  supported `0.1.0` runtime.
- **Relevant files or artefacts not inspected:** private quarantined research
inputs excluded from Git; live Cloudflare, PyPI, and final GitHub control state.
- **Commands run:** package and Recon Rodeo unittest discovery, Ruff, mypy,
source verifier, npm database checks, Node/Bash syntax checks, Python builds,
Git status/diff checks, and the strict Stickler report validator.
- **Verification:** 9 package tests, 13 Recon Rodeo tests, Ruff, mypy, source
  inventory, Node database checks, Git whitespace checks, and reproducible
  Python artefact construction.

## Subagent Coverage

- **Used:** scout lane mapped scope, invariants, test gaps, and deployment
surfaces;
- Correctness lane reviewed CLI parsing, workflow evidence retention, installer
  ownership, case export, Python compatibility, evidence bytes, and database
  semantics.
- Security/privacy lane reviewed unauthenticated endpoints, SSRF boundaries,
  research provenance, CI permissions, and Worker exposure.
- Verifier lane reviewed CI coverage, D1 migration/deployment readiness,
  publication gates, and acceptance evidence.
- **Not used:** no additional lanes beyond the four named review roles.
- **Synthesis notes:** all promoted findings were reproduced or confirmed
against the working tree; unsupported candidates were discarded.

## Findings

### Critical

None found.

### High

None found.

### Medium

None found.

### Low / Suggestions / Nits

- Live Cloudflare deployment should add account-level Access/rate-limit policy
  where per-user identity or abuse controls are required.
- PyPI environment protection and trusted-publisher binding remain publication
  setup tasks, not source-tree defects.

## Needs Verification

- Final clean GitHub CI after replacing `main` with the single root commit.
- GitHub ruleset, code-scanning, secret-scanning, Dependabot, and environment
  readback.
- Fresh-account `ospo-db` deployment, D1 backup/restore, unauthenticated 401,
  authenticated non-destructive call, and migration smoke test.
- Non-publishing release-workflow run after the protected `v0.1.0` tag exists.

## What Looks Solid

- The package contains the advertised workflow and agent resources.
- Installer ownership, collisions, project moves, and interrupted writes fail
  conservatively.
- Workflow receipts are case/task-bound and completion evidence is retained.
- Acquisition receipts hash original bytes and state their proof limits.
- `ospo-db` is correctly documented as the recommended database and is covered
  by authentication, integrity checks, migration, tests, CI, and Dependabot.
- Actions are SHA-pinned with least-privilege permissions; release publication
  uses a protected environment and OIDC.

## Fix Plan

All repository blockers found during this review were fixed and regression
coverage was added. The remaining sequence is operational: create the root
commit, replace `main`, obtain green CI, apply/read back repository controls,
and stop before tag or package publication.

## Residual Risk

No local review can prove Cloudflare, GitHub, or PyPI account configuration.
The repository encodes fail-closed defaults and verification steps, while live
deployment and publication remain explicitly gated.
