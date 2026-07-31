# Release process

The first release is blocked until local Gates A and B pass. GitHub and publishing
work begins only after that evidence exists.

## Gate A: source truth

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s src/skills/recon-rodeo/scripts -p 'test_*.py' -v
python3 scripts/verify_release.py --source .
```

The verifier checks version agreement, package resources, research admission,
structured files, prohibited debris, and release-facing claims.

## Gate B: reproducible artefacts

```bash
python3 -m build --sdist
python3 -m pip wheel --no-deps --wheel-dir dist dist/*.tar.gz
python3 scripts/verify_release.py --dist dist
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

After local gates pass, create the repository, verify inherited community-health
files, add `bug` and `enhancement` labels, enable intended security controls, and
protect `main` after CI exists. Require review, CI, and conversation resolution.

## Gate D: publication

Complete two owner review passes, tag the reviewed commit, and publish only from
the protected GitHub environment using trusted publishing. Read back the tag,
workflow run, release artefacts, checksums, and package page before announcement.
Use a corrective release rather than rewriting a published tag.
