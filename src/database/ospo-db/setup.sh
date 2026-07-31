#!/usr/bin/env bash
set -euo pipefail

# ospo-db :: one-command setup
# Creates D1 database, applies schema, configures authentication, deploys worker.
# Prerequisites: wrangler and openssl installed; wrangler authenticated.

cd "$(dirname "$0")"
mkdir -p .wrangler
chmod 700 .wrangler
DEPLOY_CONFIG=".wrangler/ospo-db.jsonc"
TOKEN_FILE=".wrangler/ospo-db-token"
CONNECTOR_FILE=".wrangler/mcp.json"

echo ""
echo "  ospo-db :: setup"
echo "  ────────────────────────"
echo ""

# 1. Create D1 database
echo "  Creating D1 database..."
DB_OUTPUT=$(wrangler d1 create ospo-db 2>&1) || {
  if echo "$DB_OUTPUT" | grep -q "already exists"; then
    echo "  Database 'ospo-db' already exists, fetching ID..."
    DB_ID=$(wrangler d1 list --json 2>/dev/null | python3 -c '
import json
import sys

matches = [
    item.get("uuid") or item.get("id")
    for item in json.load(sys.stdin)
    if item.get("name") == "ospo-db"
]
matches = [value for value in matches if value]
if len(matches) != 1:
    raise SystemExit("Expected exactly one D1 database named ospo-db")
print(matches[0])
')
  else
    echo "  Error creating database:"
    echo "$DB_OUTPUT"
    exit 1
  fi
}

# Extract database ID from creation output
if [ -z "${DB_ID:-}" ]; then
  DB_ID=$(echo "$DB_OUTPUT" | grep -oP '"database_id":\s*"\K[^"]+' || \
          echo "$DB_OUTPUT" | grep -oP 'database_id\s*=\s*"\K[^"]+' || \
          echo "$DB_OUTPUT" | grep -oP '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
fi

if [ -z "${DB_ID:-}" ]; then
  echo "  Could not extract database ID. Output was:"
  echo "$DB_OUTPUT"
  echo ""
  echo "  Create manually: wrangler d1 create ospo-db"
  echo "  Then paste the ID into wrangler.jsonc and run:"
  echo "    wrangler d1 execute ospo-db --file=schema.sql"
  echo "    wrangler deploy"
  exit 1
fi

echo "  ✓ Database ID: $DB_ID"

# 2. Create a private deployment configuration with the actual database ID.
python3 - "$DB_ID" "$DEPLOY_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

database_id, destination = sys.argv[1:]
config = {
    "name": "ospo-db",
    "main": "worker.js",
    "compatibility_date": "2025-03-07",
    "observability": {"enabled": True},
    "d1_databases": [
        {
            "binding": "DB",
            "database_name": "ospo-db",
            "database_id": database_id,
        }
    ],
}
Path(destination).write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PY
chmod 600 "$DEPLOY_CONFIG"
echo "  ✓ Created private deployment configuration"

# 3. Apply schema
echo "  Applying schema..."
wrangler d1 execute ospo-db --config "$DEPLOY_CONFIG" --file=schema.sql --yes > /dev/null 2>&1
if ! wrangler d1 execute ospo-db --config "$DEPLOY_CONFIG" \
  --command "SELECT completion_records FROM progress LIMIT 0" --yes > /dev/null 2>&1; then
  wrangler d1 execute ospo-db --config "$DEPLOY_CONFIG" \
    --file=migrations/0001_completion_records.sql --yes > /dev/null 2>&1
  echo "  ✓ Progress schema migrated"
fi
echo "  ✓ 9 tables created"

# 4. Create and install a bearer secret without printing it.
if [ ! -s "$TOKEN_FILE" ]; then
  openssl rand -hex 32 > "$TOKEN_FILE"
  chmod 600 "$TOKEN_FILE"
fi
wrangler secret put OSPO_DB_TOKEN --config "$DEPLOY_CONFIG" < "$TOKEN_FILE" > /dev/null
echo "  ✓ Authentication secret installed"

# 5. Deploy
echo "  Deploying worker..."
DEPLOY_OUTPUT=$(wrangler deploy --config "$DEPLOY_CONFIG" 2>&1)
WORKER_URL=$(echo "$DEPLOY_OUTPUT" | grep -oP 'https://[^\s]+workers\.dev' | head -1)

if [ -z "$WORKER_URL" ]; then
  echo "  Deployment completed, but the Worker URL could not be read."
  exit 1
fi

python3 - "$WORKER_URL" "$TOKEN_FILE" "$CONNECTOR_FILE" <<'PY'
import json
import sys
from pathlib import Path

worker_url, token_path, destination = sys.argv[1:]
token = Path(token_path).read_text(encoding="utf-8").strip()
config = {
    "mcpServers": {
        "ospo-db": {
            "url": f"{worker_url}/mcp",
            "headers": {"Authorization": f"Bearer {token}"},
        }
    }
}
Path(destination).write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PY
chmod 600 "$CONNECTOR_FILE"

echo "  ✓ Deployed"
echo ""
echo "  ────────────────────────"
echo "  MCP endpoint: ${WORKER_URL}/mcp"
echo "  Private connector config: $(pwd)/$CONNECTOR_FILE"
echo ""
echo "  Import the private connector config; do not share or commit it."
echo "  26 tools ready. Run an investigation."
echo ""
