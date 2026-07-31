#!/usr/bin/env python3
"""
ospo :: first-pass orchestrator
Runs a safe passive OSINT collection bundle for an entity, domain, URL, email, phone, coordinate, or crypto address.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from case_manager import CaseManager
from osint_common import JsonlAuditLog, ensure_dir, slugify, utc_now, write_json
from search_intel import SearchIntelligence
from news_monitor import NarrativeMonitor
from web_archive_intel import ArchiveIntel
from public_records import PublicRecordsCollector
from email_intel import EmailIntel
from phone_intel import PhoneIntel
from blockchain_intel import BlockchainIntel
from geospatial_context import GeospatialContext


EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)
URL_RE = re.compile(r"^https?://", re.I)
COORD_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$")


class PassiveOSINTOrchestrator:
    def __init__(self, case_root: str = "./cases"):
        self.case_root = case_root
        self.cm = CaseManager(case_root)

    def classify_seed(self, seed: str) -> str:
        if EMAIL_RE.match(seed):
            return "email"
        if URL_RE.match(seed):
            return "url"
        if COORD_RE.match(seed):
            return "coordinate"
        if seed.startswith("+") or re.sub(r"\D", "", seed).isdigit() and len(re.sub(r"\D", "", seed)) >= 8:
            return "phone"
        if seed.startswith("0x") or seed.startswith("bc1") or (seed and seed[0] in "13" and len(seed) > 25):
            return "crypto"
        if "." in seed and " " not in seed:
            return "domain"
        return "entity"

    def run(self, seed: str, analyst: str = "ospo") -> dict[str, Any]:
        case = self.cm.create_case(f"OSINT first pass - {seed}", analyst=analyst, description="Passive first-pass collection bundle")
        case_dir = Path(case["case_dir"])
        processed = ensure_dir(case_dir / "processed")
        reports = ensure_dir(case_dir / "reports")
        audit = JsonlAuditLog(case_dir / "logs" / "audit.jsonl")
        seed_type = self.classify_seed(seed)
        audit.write("seed_classified", seed=seed, seed_type=seed_type)
        outputs: dict[str, Any] = {"case": case, "seed": seed, "seed_type": seed_type, "started_at_utc": utc_now(), "outputs": []}

        def add(name: str, data: dict[str, Any]) -> None:
            path = processed / f"{name}.json"
            write_json(path, data)
            outputs["outputs"].append({"name": name, "path": str(path), "summary_keys": list(data.keys())[:20]})
            audit.write("module_completed", module=name, path=str(path))

        # Universal collection
        add("search_intel", SearchIntelligence(str(processed / "search")).source_leads_for_entity(seed))
        add("news_monitor", NarrativeMonitor(str(processed / "news")).collect(f'"{seed}"', timespan="1month"))
        add("public_records", PublicRecordsCollector(str(processed / "public_records")).investigate(seed))

        if seed_type in {"url", "domain"}:
            url = seed if seed_type == "url" else f"https://{seed}"
            add("archive_intel", ArchiveIntel(str(processed / "archive")).investigate_url(url))
        elif seed_type == "email":
            add("email_intel", EmailIntel().analyse(seed))
        elif seed_type == "phone":
            add("phone_intel", PhoneIntel().analyse(seed))
        elif seed_type == "crypto":
            add("blockchain_intel", BlockchainIntel(str(processed / "blockchain")).analyse_address(seed))
        elif seed_type == "coordinate":
            m = COORD_RE.match(seed)
            if m:
                add("geospatial_context", GeospatialContext(str(processed / "geo")).context_for_point(float(m.group(1)), float(m.group(2))))

        outputs["finished_at_utc"] = utc_now()
        summary_path = reports / "first_pass_summary.json"
        write_json(summary_path, outputs)
        self.cm.index_evidence(str(case_dir))
        return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a passive OSINT first-pass bundle")
    parser.add_argument("seed")
    parser.add_argument("--case-root", default="./cases")
    parser.add_argument("--analyst", default="ospo")
    args = parser.parse_args()
    print(json.dumps(PassiveOSINTOrchestrator(args.case_root).run(args.seed, args.analyst), indent=2))


if __name__ == "__main__":
    main()
