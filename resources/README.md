# Resources

This directory separates material by audience.

- `docs/` contains operator-facing guidance, policy, provenance, and research
  notes.
- `build/` contains the in-tree PEP 517 backend and its reviewed
  source-distribution inventory.
- `dev/` contains maintainer-only tests, release verification, audit records,
  and the repository design skill.

The source distribution contains `docs/` and the small build backend. The
backend admits those public resources directly, without extra build-control
files at the repository root. `dev/` remains in the repository for maintainers
and is excluded from package artefacts. Installing an OSINT framework need not
also appoint the operator to the release engineering team.
