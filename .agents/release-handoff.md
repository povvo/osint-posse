# Release Handoff

Repository: `osint-posse` source tree; GitHub repository not yet created

Branch: Not created

Commit SHA: Not created

Version: `0.1.0`

Tag: Intended `v0.1.0`; not created

## Summary

The local source and reproducible-artefact gates pass. This handoff authorises no publication: it prepares the verified inputs and enumerates the remote evidence required for the first repository and release.

## Changes

- Packaged Recon Rodeo and both 60-agent definition sets into the Python wheel.
- Replaced overwrite-prone lifecycle operations with project-default, dry-run, collision-preflighted, SHA-256 ownership-aware install and uninstall.
- Reconciled `ospo` and `green-ink` command contracts and made workflow, template, tool, setup, and doctor surfaces available after installation.
- Repaired workflow fixtures and evidence-preservation language and metadata.
- Replaced fictional `1.0.0` history and publication claims with a truthful `0.1.0` pre-release state.
- Added responsible-use, privacy/data-handling, security-model, evidence/provenance, and release-process documentation.
- Quarantined raw research pending explicit per-file redistribution decisions.
- Added pinned CI, release, dependency-update, source-verification, and distribution-inventory definitions for the future repository.

## Verification Evidence

- Package suite: 7 of 7 tests pass.
- Recon Rodeo suite: 10 of 10 tests pass.
- Source gate: 710 release-eligible paths; path-inventory SHA-256 `aff389f7f00d91294f42f0e8858af9e7df62f59411b61ce823d59e564205803a`.
- Initial Git staging: 710 paths; release-payload blob-manifest SHA-256 `f5ce4de2a9f538990d7178fd2b3da28f2091b1ec57257dc46ad2ff0591b95cd7`, excluding these two self-referential audit records. Content identity becomes the reviewed Git commit SHA at Gate C.
- Sdist: `/tmp/osint-posse-final-dist-20260731-r3/osint_posse-0.1.0.tar.gz`; 348 members; SHA-256 `3b23647b371b5d618fcfe021c12a0cf644026baf7a05b6ece18381953c6ce448`.
- Wheel rebuilt from that sdist: `/tmp/osint-posse-final-dist-20260731-r3/osint_posse-0.1.0-py3-none-any.whl`; 265 members; SHA-256 `60b48dd9f029d1caa608e16ac03c2abf4ffbb98448983900361a7fbac97a6ac6`.
- Installed inventory: Recon Rodeo, 60 Claude agents, 60 Codex agents, 56 task cards, and 21 templates.
- Lifecycle smoke test: 250 files installed and 250 files removed; dry-run counts agreed; no file or symlink residue remained.

## CI

Not run because no GitHub repository exists. After initial import, CI must pass at the reviewed `main` commit on Python 3.10 through 3.14, including the source gate, both test suites, sdist-to-wheel build, distribution inventory, clean-install smoke test, and secret scan.

## Documentation

The README, changelog, release process, responsible-use boundary, privacy/data-handling model, security model, and evidence/provenance model now describe the pre-release product. Owner community-health files are intended to inherit after repository creation and must be read back then.

## Breaking Changes

There is no prior public release. Relative to the old source tree, the working version is `0.1.0`; installation defaults to project scope; unowned or modified collisions fail closed; profiling is explicit rather than mandatory; and evidence output is described as an acquisition receipt rather than forensic-grade chain of custody.

## Migration

No public-user migration exists. Any private checkout using the earlier lifecycle commands should run `ospo install --dry-run`, resolve reported collisions, then install into project scope. Existing investigator-created files are not claimed or removed.

## Rollback

Before publication, discard a candidate commit or rebuild from the last reviewed source manifest. After publication, do not move or replace `v0.1.0`; withdraw the affected package artefact if necessary, document impact, repair on a new commit, and issue a corrective version.

## Release Notes

Draft from `[Unreleased]` only after the reviewed release commit is fixed. The first public notes must describe actual shipped behaviour and must not claim CI, package availability, provenance, or support state until each surface has been read back.

## Follow-up

1. Initialise the repository from the verified staging set; confirm generated files, sidecars, secrets, and quarantined raw research are absent.
2. Create the GitHub repository with `main`, issues, `bug` and `enhancement` labels, inherited community-health files, Dependabot, secret scanning, supported code scanning, and protected-branch controls.
3. Obtain the two owner-required review passes and a green CI run at the exact release commit.
4. Configure the protected `pypi` environment and PyPI trusted publishing without a long-lived package token.
5. Create `v0.1.0`, run the release workflow with publication initially disabled, compare workflow artefact checksums, then explicitly approve publication.
6. Read back the tag, release, workflow, and package page before announcing availability.
