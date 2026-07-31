# ospo-db

`ospo-db` is the recommended persistent investigation database for OSINT Posse:
an authenticated 26-tool MCP service backed by Cloudflare D1. It stores
investigations, entities, relationships, source grades, timelines, evidence,
locations, notebooks, and workflow progress across sessions.

Green Ink is the workflow CLI. Its local `.green-ink` files contain the
minimum state needed to operate the task runner when `ospo-db` is unavailable
or deliberately not deployed. Those files are not a database and do not
provide the database tool surface.

Run `./setup.sh` from this directory after authenticating Wrangler. The script
selects or creates the exact `ospo-db` database, writes a private deployment
configuration, applies the schema, creates a 256-bit bearer secret, deploys the
Worker, and writes an owner-readable connector configuration under
`.wrangler/mcp.json`. Nothing under `.wrangler/` may be committed.

Existing pre-release databases that lack `completion_records` must apply
`migrations/0001_completion_records.sql` once before deploying this version:

```bash
wrangler d1 execute ospo-db \
  --config .wrangler/ospo-db.jsonc \
  --file migrations/0001_completion_records.sql \
  --yes
```

The `/mcp` endpoint fails closed when the secret is absent and returns `401` for
missing or invalid bearer credentials. Permanent delete tools additionally
require their explicit confirmation argument. Back up D1 before destructive
operations or schema migration.
