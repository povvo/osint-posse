# Release process

The first release is blocked until local Gates A and B pass. GitHub and publishing
work begins only after that evidence exists.

## Gate A: source truth

```bash
PYTHONPATH=src python3 -m unittest discover -s resources/dev/tests -v
python3 -m unittest discover -s resources/dev/tests/recon_rodeo -p 'test_*.py' -v
python3 resources/dev/scripts/verify_release.py --source .
ruff check src/ospo resources/build/ospo_build_backend.py resources/dev/tests resources/dev/scripts
mypy src/ospo
```

The verifier checks version agreement, package resources, research admission,
structured files, prohibited debris, release-facing claims, locked MCP
dependencies, Dependabot coverage, and required CI gates.

For each directory under `src/tools/recommended/mcp` that contains a
`package-lock.json`, run:

```bash
npm ci
npm audit --omit=dev --audit-level=moderate
npm run typecheck
npm run build
```

These checks validate the source-only Cloudflare Workers. They do not authorise
or perform a deployment.

## Gate B: reproducible artefacts

```bash
python3 -m build --sdist
python3 -m pip wheel --no-deps --wheel-dir dist dist/*.tar.gz
python3 resources/dev/scripts/verify_release.py --dist dist
```

Install the wheel built from the sdist in a clean environment and run:

```bash
ospo --help
ospo doctor
ospo workflow --help
ospo tool list
green-ink doctor
```

Record artefact SHA-256 values and the verifier’s member inventory. Build output
is evidence about that build, not about an absent tag.

## Gate C: repository controls

After local gates pass, verify inherited community-health files, the `bug` and
`enhancement` labels, dependency and secret scanning, supported code scanning,
and repository settings. Protect `main` after its first successful CI run.
Require review, CI, linear history, and conversation resolution; prohibit force
push and branch deletion.

## Gate D: publication

Complete two owner review passes, tag the reviewed commit, and publish only from
the protected GitHub environment using trusted publishing. The workflow builds
the wheel from the sdist, verifies both distributions, records SHA-256
checksums, and creates GitHub artifact attestations before publication. Read
back the tag, workflow run, release artefacts, checksums, attestations, and
package page before announcement. Use a corrective release rather than
rewriting a published tag.
