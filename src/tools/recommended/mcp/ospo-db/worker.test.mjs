import assert from "node:assert/strict";
import test from "node:test";

import worker from "./worker.js";

const TOKEN = "a".repeat(64);

function request(body, token = TOKEN) {
  const headers = {"content-type": "application/json"};
  if (token !== null) headers.authorization = `Bearer ${token}`;
  return new Request("https://ospo-db.example/mcp", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
}

function fakeDatabase(progress = null) {
  const operations = [];
  return {
    operations,
    async batch(statements) {
      return Promise.all(statements.map((statement) => statement.run()));
    },
    prepare(sql) {
      const operation = {sql, bindings: []};
      operations.push(operation);
      return {
        bind(...bindings) {
          operation.bindings = bindings;
          return this;
        },
        async first() {
          if (sql.startsWith("SELECT*FROM progress")) return progress;
          if (sql.startsWith("SELECT COUNT(*)")) return {c: 0};
          return null;
        },
        async run() {
          return {success: true};
        },
      };
    },
  };
}

function call(name, args = {}) {
  return {
    jsonrpc: "2.0",
    id: 1,
    method: "tools/call",
    params: {name, arguments: args},
  };
}

test("MCP requests fail closed when authentication is not configured", async () => {
  const response = await worker.fetch(request({jsonrpc: "2.0", id: 1, method: "tools/list"}), {DB: fakeDatabase()});
  assert.equal(response.status, 503);
});

test("MCP requests reject missing and incorrect bearer tokens", async () => {
  for (const candidate of [null, "wrong"]) {
    const response = await worker.fetch(
      request({jsonrpc: "2.0", id: 1, method: "tools/list"}, candidate),
      {DB: fakeDatabase(), OSPO_DB_TOKEN: TOKEN},
    );
    assert.equal(response.status, 401);
  }
});

test("progress round-trips verified completion records", async () => {
  const completionRecords = {
    "1.1": {
      manifest_sha256: "1".repeat(64),
      task_sha256: "2".repeat(64),
      notebook_sha256: "3".repeat(64),
    },
  };
  const db = fakeDatabase({
    current_index: 1,
    completed: "[\"1.1\"]",
    completion_records: JSON.stringify(completionRecords),
  });
  const response = await worker.fetch(
    request(call("load_progress", {investigation_id: "INV-test"})),
    {DB: db, OSPO_DB_TOKEN: TOKEN},
  );
  assert.equal(response.status, 200);
  const payload = await response.json();
  const content = JSON.parse(payload.result.content[0].text);
  assert.deepEqual(content.completion_records, completionRecords);
});

test("authenticated destructive operations remain confirmation-gated", async () => {
  const denied = await worker.fetch(
    request(call("delete_investigation", {investigation_id: "INV-test", confirm: false})),
    {DB: fakeDatabase(), OSPO_DB_TOKEN: TOKEN},
  );
  const deniedPayload = await denied.json();
  assert.match(deniedPayload.result.content[0].text, /confirm:true/);

  const db = fakeDatabase();
  const allowed = await worker.fetch(
    request(call("delete_investigation", {investigation_id: "INV-test", confirm: true})),
    {DB: db, OSPO_DB_TOKEN: TOKEN},
  );
  assert.equal(allowed.status, 200);
  assert.ok(db.operations.some(({sql}) => sql === "DELETE FROM investigations WHERE id=?"));
});
