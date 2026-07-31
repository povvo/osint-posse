# Security model

OSINT Posse assumes the operator controls the local machine and case workspace.
It treats collected content, URLs, documents, service responses, and generated
artefacts as untrusted.

## Protected boundaries

- Public-source requests validate destinations and bound redirects, response
  size, and time.
- Workflow state rejects traversal, links, malformed JSON, and non-contiguous
  progression.
- Installation preflights every destination and records owned file hashes.
- Uninstall leaves modified and unrelated files in place.
- Standalone tools require an explicit mode and do not advance workflow state.
- The release verifier rejects generated debris, secrets, unclassified research,
  and incomplete package resources from release artefacts.

## Not provided

- A sandbox for every experimental script.
- Endpoint protection, disk encryption, identity management, or backup control.
- Proof that an external source, MCP server, model, or operator is trustworthy.
- Continuous chain of custody or legal admissibility.
- Automatic enforcement of investigative authority or retention decisions.

Run experimental tools only after code review and with the minimum filesystem,
network, credential, and data access needed. Report vulnerabilities through the
owner-level private security route after repository creation; verify that route
before the first public release.
