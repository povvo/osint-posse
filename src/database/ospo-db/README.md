# ospo-db

`ospo-db` is the recommended persistent investigation database for OSINT Posse:
an authenticated 26-tool MCP service backed by Cloudflare D1. Investigations,
entities, relationships, source grades, timelines, evidence, locations,
notebooks, and workflow progress all survive between sessions.

## Deploy

The database Worker has no unauthenticated one-click deployment. From this
directory, authenticate Wrangler and run:

```bash
./setup.sh
```

The script selects or creates the exact `ospo-db` D1 database, writes a private
deployment configuration, applies the schema, creates a 256-bit bearer secret,
deploys the Worker, and writes an owner-readable connector configuration under
`.wrangler/mcp.json`. Nothing under `.wrangler/` may be committed.

## Tools

| Domain | Tools |
| --- | --- |
| Investigation | `create_investigation`, `list_investigations`, `load_investigation`, `close_investigation`, `update_investigation`, `delete_investigation` |
| Entities | `add_entity`, `search_entities`, `update_entity`, `delete_entity` |
| Relationships | `add_relationship`, `get_relationships`, `update_relationship`, `delete_relationship`, `search_relationships`, `get_neighbors` |
| Source grading | `record_grade` |
| Timeline | `add_timeline_event`, `get_timeline` |
| Progress | `save_progress`, `load_progress` |
| Notebook | `save_notebook`, `load_notebook` |
| Evidence | `register_evidence` |
| Geo | `add_location` |
| Statistics | `get_statistics` |

These 26 tools are the investigation database surface.

## Migration, backup, authentication, and rollback

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
