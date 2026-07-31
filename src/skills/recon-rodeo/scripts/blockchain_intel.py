#!/usr/bin/env python3
"""
ospo :: blockchain intelligence
Passive blockchain address and transaction context for BTC and ETH.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict, field
from typing import Any

from osint_common import PublicSourceClient, ensure_dir, slugify, utc_now, write_json

BTC_RE = re.compile(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,90}$")
ETH_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")


@dataclass
class BlockchainResult:
    chain: str
    address: str
    summary: dict[str, Any] = field(default_factory=dict)
    transactions: list[dict[str, Any]] = field(default_factory=list)
    risk_notes: list[str] = field(default_factory=list)
    collected_at_utc: str = field(default_factory=utc_now)


class BlockstreamClient:
    BASE = "https://blockstream.info/api"

    def __init__(self, http: PublicSourceClient):
        self.http = http

    def address(self, address: str) -> dict[str, Any]:
        return self.http.get_json(f"{self.BASE}/address/{address}", cache_ttl_seconds=300)  # type: ignore[return-value]

    def txs(self, address: str) -> list[dict[str, Any]]:
        data = self.http.get_json(f"{self.BASE}/address/{address}/txs", cache_ttl_seconds=300)
        return data if isinstance(data, list) else []


class EtherscanClient:
    BASE = "https://api.etherscan.io/api"

    def __init__(self, http: PublicSourceClient, api_key: str | None = None):
        self.http = http
        self.api_key = api_key or os.getenv("ETHERSCAN_API_KEY")

    def balance(self, address: str) -> dict[str, Any]:
        if not self.api_key:
            return {"skipped": "ETHERSCAN_API_KEY not set"}
        return self.http.get_json(self.BASE, params={"module": "account", "action": "balance", "address": address, "tag": "latest", "apikey": self.api_key}, cache_ttl_seconds=300)  # type: ignore[return-value]

    def txs(self, address: str, limit: int = 25) -> list[dict[str, Any]]:
        if not self.api_key:
            return []
        data = self.http.get_json(self.BASE, params={"module": "account", "action": "txlist", "address": address, "startblock": 0, "endblock": 99999999, "page": 1, "offset": limit, "sort": "desc", "apikey": self.api_key}, cache_ttl_seconds=300)
        return data.get("result", []) if isinstance(data, dict) else []


class BlockchainIntel:
    def __init__(self, output_dir: str = "./blockchain_intel"):
        self.output_dir = ensure_dir(output_dir)
        http = PublicSourceClient(cache_dir=self.output_dir / "cache", min_interval_seconds=1.0)
        self.btc = BlockstreamClient(http)
        self.eth = EtherscanClient(http)

    def classify(self, address: str) -> str:
        if ETH_RE.match(address):
            return "ethereum"
        if BTC_RE.match(address):
            return "bitcoin"
        return "unknown"

    def analyse_address(self, address: str) -> dict[str, Any]:
        chain = self.classify(address)
        result = BlockchainResult(chain=chain, address=address)
        if chain == "bitcoin":
            result.summary = self.btc.address(address)
            result.transactions = self.btc.txs(address)[:25]
        elif chain == "ethereum":
            result.summary = self.eth.balance(address)
            result.transactions = self.eth.txs(address)
        else:
            result.risk_notes.append("Address format not recognised as BTC or ETH")
        self._annotate(result)
        data = asdict(result)
        out = self.output_dir / f"blockchain_{slugify(address)}.json"
        write_json(out, data)
        data["output_path"] = str(out)
        return data

    @staticmethod
    def _annotate(result: BlockchainResult) -> None:
        if result.chain == "bitcoin" and isinstance(result.summary, dict):
            stats = result.summary.get("chain_stats", {})
            funded = stats.get("funded_txo_sum", 0)
            spent = stats.get("spent_txo_sum", 0)
            if funded and funded == spent:
                result.risk_notes.append("fully_spent_address")
        if len(result.transactions) >= 25:
            result.risk_notes.append("transaction_list_truncated")


def main() -> None:
    parser = argparse.ArgumentParser(description="Passive BTC/ETH address context")
    parser.add_argument("address")
    parser.add_argument("--out-dir", default="./blockchain_intel")
    args = parser.parse_args()
    print(json.dumps(BlockchainIntel(args.out_dir).analyse_address(args.address), indent=2))


if __name__ == "__main__":
    main()
