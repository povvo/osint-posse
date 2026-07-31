# Initial Repository and Release Audit

Repository: `osint-posse`
Stage: Pre-repository source tree; preparing the first GitHub import and first public release
Audit date: 2026-07-31
Release target: `v0.1.0` is the working first-release version unless the maintainer selects another version before tagging
Decision: Ready for initial GitHub repository creation; package publication remains gated on remote controls and the maintainer's release decision

## Reader outcome

This report defines what must change before this directory becomes a public GitHub repository or a published Python package. It does not treat missing remote state as a defect. There is no repository, tag, release, Actions history, branch rule, or PyPI project yet; claims about those things would be correspondence addressed to a building that has not been constructed.

## Scope and evidence

Inspected: Root package metadata and documentation; all `ospo` modules; the Recon Rodeo skill, command layer, task runner, state tests, and evidence capture path; agent and task inventories; research artefacts; owner community-health defaults; build output from a fresh local sdist/wheel build; structured-file syntax; and the current release-facing claims.

Out of scope: Creating the GitHub repository; publishing a tag, GitHub release, or PyPI package; changing remote rules or security settings; deciding redistribution rights for third-party research; live Cloudflare deployment; and legal advice about investigative use.

Evidence boundary: Local checks establish source-tree and artefact readiness. They do not establish investigative correctness, legal authority, live service availability, or release provenance from trusted CI.

## Readiness checklist

Repository: Pass for Gate A/B; the intentionally unpublished source tree and locally verified release artefacts exist
Issue/PR split: Pass for this pre-repository stage; issue and pull-request policy becomes verifiable after repository creation
Trust files: Pass for initial import; release claims are source-accurate and project-specific use, privacy, security, and evidence boundaries are documented
Capacity: Pass
Quickstart: Pass; the documented package, workflow, and build commands agree with clean-installed command help and fixtures
Funding route: Pass
Stop rules: Pass for initial import; publishing remains gated until trusted CI, tag provenance, environment approval, and package-page readback exist
Decision: Pass

This capacity result covers repository bootstrap only; it makes no public response-time or availability promise. The funding route is inherited owner context and supports no income or service-entitlement claim. The decision means that the initial repository may be created from the verified staging set; Gates C and D still precede any `v0.1.0` announcement or package publication.

## Trust-file audit

README: Pass; it identifies the project as pre-release and makes no CI, repository, issue-route, PyPI, or release-history claim
Licence: Pass; MIT licence text is present
Contributing: Pass by intended owner inheritance; verify inheritance after repository creation
Security: Pass for initial import; owner-level vulnerability reporting is intended to inherit, and project-specific security and data-handling boundaries are present
Support: Pass by intended owner inheritance; do not promise response windows beyond the owner policy
Funding: Pass by intended owner inheritance; no income, tax, or outcome claim is made
Issue templates: Pass by intended owner inheritance; create the `bug` and `enhancement` labels during repository bootstrap
PR template: Pass by intended owner inheritance
Accessibility: Pass for text status labels; existing visual assets were not altered or re-originated
Missing evidence: Trusted CI run, repository settings readback, reviewed commit SHA, signed or otherwise approved tag, PyPI environment approval, package-page readback, and any positive decision to redistribute quarantined research
Trust-file conclusion — initial import may proceed; public package publication may not.

## Baseline observations

| Check | Result | Evidence |
| --- | --- | --- |
| Python syntax | Pass | 313 Python files parsed |
| JSON syntax | Pass | 14 JSON files parsed |
| TOML syntax | Pass | 61 TOML files parsed |
| Agent inventory | Pass | 60 Claude definitions and 60 Codex definitions |
| Task inventory | Pass | 56 task cards discovered by the task-runner filename contract |
| Unit tests | Fail | 7 tests run; 2 stale state-schema assertions fail |
| Baseline build | Fail as a product artefact | Build succeeds, but the wheel contains only the small `ospo` package and `ospo/data/README`; Recon Rodeo and both agent packs are absent |
| Source hygiene | Fail | Generated egg metadata and Windows `Zone.Identifier` sidecars are present |
| Raw research provenance | Fail | 12 PDFs and 7 raw JSON exports have no complete redistribution ledger |

These observations are the measured starting point, not the current state. They are retained so that the repair has an auditable before-and-after record.

## Remediation and current validation

| Gate | Result | Evidence |
| --- | --- | --- |
| Package tests | Pass | 7 of 7 tests pass, including collision, ownership, modified-file preservation, project/user scope, and symlink-escape rejection |
| Recon Rodeo tests | Pass | 10 of 10 state and acquisition-receipt tests pass |
| Source verifier | Pass | 710 release-eligible paths; path-inventory SHA-256 `aff389f7f00d91294f42f0e8858af9e7df62f59411b61ce823d59e564205803a`; structured-file, secret-pattern, documentation-claim, version-lock, inventory, and provenance-ledger checks pass |
| Initial Git staging | Pass | 710 paths; release-payload blob-manifest SHA-256 `f5ce4de2a9f538990d7178fd2b3da28f2091b1ec57257dc46ad2ff0591b95cd7` (excluding the self-referential audit and handoff records); no ignored release-debris pattern appears in the index; `git diff --cached --check` passes |
| Source distribution | Pass | 348 members, including linked public release documentation while excluding raw research; SHA-256 `3b23647b371b5d618fcfe021c12a0cf644026baf7a05b6ece18381953c6ce448` |
| Wheel rebuilt from sdist | Pass | 265 members; SHA-256 `60b48dd9f029d1caa608e16ac03c2abf4ffbb98448983900361a7fbac97a6ac6` |
| Installed resource inventory | Pass | Recon Rodeo, 60 Claude agents, 60 Codex agents, 56 task cards, and 21 templates resolve from the installed wheel |
| CLI smoke test | Pass | `ospo --help`, `doctor`, workflow help, template help, tool inventory, and `green-ink doctor` execute from the clean environment |
| Install/uninstall smoke test | Pass | Dry run and live operations each account for 250 files; uninstall leaves no file or symlink residue |
| Workflow contract | Pass | The documented evidence-manifest sequence rejects incomplete evidence and advances exactly one of 56 tasks when complete |
| Research boundary | Pass for initial import | Raw PDFs and exports remain quarantined and ignored; the empty admissions ledger has the required schema |
| Remote controls | Pending by design | No repository, workflow run, branch rule, tag, release, or package project exists yet |

## Findings

### R1 — The distribution does not contain the advertised product

Severity: Blocker
Evidence: `pyproject.toml` discovers only `ospo*`; `ospo/_paths.py` expects resources under `ospo/data` and a sibling `src`; the built wheel contains neither `src/skills/recon-rodeo` nor the Claude/Codex agent definitions.
Impact: A clean package install cannot perform the first documented `ospo install`.
Repair: Make the sdist self-contained and copy canonical release resources into the wheel during the normal build. Resolve installed resources from the package and source-checkout resources from an explicit development fallback.
Target files: `pyproject.toml`, `MANIFEST.in`, `setup.py`, `ospo/_paths.py`, package tests
Acceptance: A wheel built from the sdist contains Recon Rodeo, 60 Claude agents, and 60 Codex agents; a clean environment can run the installed CLI without the source tree.

### R2 — Install and uninstall do not know which files they own

Severity: Blocker
Evidence: `ospo/_install.py` overwrites matching destinations with `shutil.copy2`; skill uninstall removes the complete destination tree; agent uninstall removes matching filenames without hashes or an ownership record.
Impact: Installing can replace user work and uninstalling can delete it. Packaging this behaviour would convert a release into a small file-loss lottery.
Repair: Default to project scope; provide an explicit user scope; preflight every destination; refuse unowned collisions; support `--dry-run`; record SHA-256 ownership; and remove only unchanged, owned files.
Target files: `ospo/_paths.py`, `ospo/_install.py`, `ospo/cli.py`, installer tests
Acceptance: Tests cover empty install, dry run, identical unowned files, conflicting files, owned update, modified installed files, unrelated files, project scope, user scope, and hash-aware uninstall.

### R3 — The documented CLI and packaged CLI are different products

Severity: Blocker
Evidence: `CHANGELOG.md` describes workflow, tool, template, doctor, and setup commands; `ospo/cli.py` exposes package lifecycle commands; `green_ink_cli.py` implements the workflow command layer but has no installed entry point.
Impact: Release notes and executable help cannot both be true.
Repair: Make `ospo` the canonical superset command and provide `green-ink` only as a documented compatibility alias to the same governed command layer.
Target files: `pyproject.toml`, `ospo/cli.py`, `ospo/_workflow.py`, CLI contract tests
Acceptance: Clean-install help and smoke tests cover lifecycle, doctor, workflow, template, tool, and setup commands through `ospo`; the compatibility alias returns the same workflow results.

### R4 — The quickstart cannot complete its own governed task

Severity: Blocker
Evidence: The README teaches plain `done`; `SKILL.md` names `--manifest`, then calls implemented manifest commands a TODO; the task runner requires `requirements --out` followed by `done --evidence-manifest`.
Impact: The main audit gate works, but its instructions route around it and then stop.
Repair: Publish one installed-command sequence and remove the stale fallback:

```text
ospo workflow init
ospo workflow next
ospo workflow requirements --out evidence-manifest.json
ospo workflow done --evidence-manifest evidence-manifest.json
ospo workflow status
```

Target files: `README.md`, `src/skills/recon-rodeo/SKILL.md`, workflow fixture tests
Acceptance: The documented sequence runs verbatim against a temporary case; incomplete evidence is rejected and a completed manifest advances exactly one task.

### R5 — No local release gate passes

Severity: Blocker
Evidence: The only discovered unit suite has two failures; no workflows exist; the README advertises a workflow that has never existed in this source tree.
Impact: There is no reviewed commit or repeatable command that proves the package can be shipped.
Repair: Fix stale tests; add repository-native CI, dependency updates, artefact inspection, clean-install CLI smoke tests, documentation checks, structured-file checks, and secret scanning. Add a trusted-publishing workflow, but do not enable or invoke it until the repository and PyPI project are configured.
Target files: `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `.github/dependabot.yml`, `scripts/verify_release.py`, tests
Acceptance: All local equivalents pass; after repository creation, the same checks pass at the intended release SHA.

### R6 — Evidence language exceeds the generated record

Severity: High
Evidence: `evidence_preservation.py` calls its output forensic-grade chain of custody while creating a synthetic WARC response with hard-coded `200 OK` and `Content-Type: text/html`; the JSON record is unsigned and is not a custody-event chain.
Impact: A byte hash proves later byte identity. It does not prove who acquired the bytes, that the WARC reproduces the response, or that custody remained continuous.
Repair: Call the current output an acquisition receipt. Preserve the actual response status, headers, final URL, redirect metadata where available, capture parameters, package version, and artefact hashes. Document what the receipt proves and does not prove. Reserve chain-of-custody language for a separately designed and verified custody-event system.
Target files: `src/skills/recon-rodeo/scripts/evidence_preservation.py`, `docs/evidence-and-provenance.md`, receipt tests/schema
Acceptance: Local HTTP fixtures cover redirects, non-200 responses, binary or rejected content, incomplete optional capture, and receipt hash verification.

### R7 — Sensitive inference is mandatory without a release boundary

Severity: High
Evidence: `SKILL.md` requires a 16-section Cognitive Surrogate Profile whenever subject information is synthesised and begins from the user's initial briefing; no project-specific responsible-use, privacy/data-handling, retention, correction, redaction, or high-impact-decision policy exists.
Impact: The workflow can persist sensitive inferences about identifiable people without a declared purpose boundary or an operator-visible choice.
Repair: Make profiling explicit and scoped rather than automatic. Document lawful-authority recording, minimisation, local and remote data flows, retention/deletion, correction, disclosure, redaction, prohibited targeting, and the ban on automated high-impact decisions.
Target files: `README.md`, `src/skills/recon-rodeo/SKILL.md`, `docs/responsible-use.md`, `docs/privacy-and-data-handling.md`, `docs/security-model.md`
Acceptance: The normal workflow does not require profiling; enabling it requires an explicit recorded decision; release docs state limitations and operator responsibilities without pretending documentation is enforcement.

### R8 — Raw research cannot enter the initial public import unclassified

Severity: High
Evidence: `docs/research` contains 12 PDFs and 7 raw JSON exports without a per-file source, author, licence, retrieval date, SHA-256, purpose, and redistribution decision.
Impact: The initial repository cannot distinguish original synthesis, public-domain or openly licensed material, private research input, and material that must not be redistributed.
Repair: Ignore raw PDFs and exports by default. Add a provenance ledger and admit an artefact only after its row records a positive redistribution decision. Keep citations and original synthesis public.
Target files: `.gitignore`, `docs/research/README.md`, `docs/research/provenance.csv`, `scripts/verify_release.py`
Acceptance: Initial Git staging contains no unclassified PDF or raw research export; every admitted artefact has a complete ledger row and matching SHA-256.

### R9 — Version and history describe a release that never occurred

Severity: High
Evidence: `pyproject.toml`, `ospo/__init__.py`, `green_ink_cli.py`, and `CHANGELOG.md` present `1.0.0` as released; there is no prior repository or release.
Impact: The first public commit would begin with fictional release history and broken comparison links.
Repair: Use `0.1.0` as the working first-release version, centralise runtime version lookup, keep all changes under `[Unreleased]`, and create the dated version section only when the release is actually cut.
Target files: `pyproject.toml`, `ospo/__init__.py`, `src/skills/recon-rodeo/scripts/green_ink_cli.py`, `CHANGELOG.md`
Acceptance: Package metadata, runtime output, artefact filenames, changelog, tag, and release title agree at publication.

### R10 — Source-tree debris can leak into the first commit

Severity: Medium
Evidence: The tree contains `osint_posse.egg-info`, build output from local verification, and `*:Zone.Identifier` sidecars; the ignore rules do not cover the sidecars.
Impact: A bulk initial add would publish generated state and transport metadata.
Repair: Extend ignore rules, reject these paths in the release verifier, and remove them from release staging before Git initialisation.
Target files: `.gitignore`, `scripts/verify_release.py`, release staging
Acceptance: The staged file manifest contains no sidecars, egg metadata, build directory, cache, environment, secret, or raw unclassified research artefact.

## Repair sequence

1. Release Gate A — local source truth
   - Package the actual supported resources.
   - Make installation ownership-safe.
   - Unify the CLI and workflow contract.
   - Fix tests and evidence terminology.
   - Replace fictional release history and public-state claims.
   - Add project-specific responsible-use and data-handling boundaries.
   - Quarantine unclassified research.

2. Release Gate B — reproducible artefacts
   - Build the sdist, then build the wheel from that sdist.
   - Inspect both manifests.
   - Install the wheel into a clean environment.
   - Run CLI, installer, workflow, docs, syntax, and secret checks.
   - Record SHA-256 checksums and the exact source-tree manifest.

3. Release Gate C — initial GitHub repository
   - Initialise Git only after the staging verifier passes.
   - Create `povvo/osint-posse` with `main` as the default branch.
   - Confirm inherited community-health files.
   - Create `bug` and `enhancement` labels.
   - Enable issues; leave wiki and Pages disabled unless separately staffed.
   - Enable Dependabot alerts, secret scanning, code scanning where supported, and branch protection after the first CI workflow exists.
   - Require pull request review, passing CI, and conversation resolution; disallow force push and branch deletion.

4. Release Gate D — first release
   - Complete the two owner-required review passes.
   - Tag the reviewed `main` commit.
   - Publish artefacts only from trusted CI.
   - Verify version agreement, checksums, release notes, install command, and rollback/corrective-release path.
   - Read back the tag, release, workflow run, and package page before announcing availability.

## Validation commands

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s src/skills/recon-rodeo/scripts -p 'test_*.py' -v
python3 scripts/verify_release.py --source .
uv build
python3 scripts/verify_release.py --dist dist
```

After a clean wheel install:

```bash
ospo --help
ospo doctor
ospo workflow --help
ospo tool list
green-ink doctor
```

## Validation results

Current result: Release Gates A and B pass. The source tree is ready for its initial GitHub import. Release Gates C and D remain intentionally open: create and configure the repository, obtain a trusted CI result at the reviewed commit, record the tag and artefact provenance, approve the protected PyPI environment, publish from trusted CI, and read back the public surfaces before announcing availability.

## Support boundary

The first release supports documented local package and workflow behaviour that passes the release fixtures. Experimental scripts, live external services, Cloudflare deployments, third-party service availability, legal conclusions, automated high-impact decisions, and unclassified research artefacts are not supported release claims.

## Trust and funding caveats

Community-file presence is not proof of enforcement. Funding-route presence is not evidence of income, capacity, or service entitlement. The repository must not add attention or publication claims until its first-success path, support boundary, and security-sensitive use boundary are legible and tested.

## Residual risks

- External data sources, APIs, service terms, and model identifiers will change after release; they need dated verification and a maintenance owner.
- Syntax and fixture tests cannot establish that every investigative technique is correct for every jurisdiction or case.
- Psychological inference, sanctions screening, identity resolution, and evidentiary use remain high-risk domains even with accurate documentation.
- Research redistribution decisions require a human rights review; the release gate can enforce the ledger but cannot invent the rights.
- Remote controls cannot be verified until the repository exists. That is expected at this stage and becomes a Gate C task, not a retrospective finding.
