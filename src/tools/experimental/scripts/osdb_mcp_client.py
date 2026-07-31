#!/usr/bin/env python3
"""OSDb MCP client manifest tool.

Builds local JSON request envelopes for OSDb-style tools and validates responses
captured from a separate MCP client. It deliberately performs no network calls.
"""
from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

TOOLS = {"create_investigation", "add_entity", "add_relationship", "search_entities", "get_graph", "update_entity"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_request(tool: str, params: dict, case_id: str) -> dict:
    if tool not in TOOLS:
        raise ValueError(f"tool must be one of {sorted(TOOLS)}")
    return {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/call", "created_at_utc": now(), "case_id": case_id, "params": {"name": tool, "arguments": params}}


def parse_pairs(values: list[str]) -> dict:
    params = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"expected key=value, got {item!r}")
        key, value = item.split("=", 1)
        params[key] = value
    return params


def validate_response(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings = []
    if "error" in data: findings.append({"severity": "error", "message": data["error"]})
    if "result" not in data and "content" not in data: findings.append({"severity": "warning", "message": "response lacks result/content"})
    return {"path": str(path), "ok": not any(f["severity"] == "error" for f in findings), "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build local OSDb MCP request envelopes or validate captured responses.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    req = sub.add_parser("request"); req.add_argument("tool", choices=sorted(TOOLS)); req.add_argument("--case-id", required=True); req.add_argument("--arg", action="append", default=[]); req.add_argument("--output")
    val = sub.add_parser("validate-response"); val.add_argument("path")
    args = ap.parse_args()
    if args.cmd == "request":
        doc = build_request(args.tool, parse_pairs(args.arg), args.case_id)
        if args.output: Path(args.output).write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(json.dumps(doc, indent=2)); return 0
    print(json.dumps(validate_response(Path(args.path)), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
