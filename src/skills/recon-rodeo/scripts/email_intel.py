#!/usr/bin/env python3
"""
ospo :: email intelligence
Low-intrusion public checks: syntax, domain DNS/MX, disposable-domain flags, Gravatar hash lookup, and search pivots.
No SMTP probing or credential/breach retrieval is performed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict, field
from typing import Any

from osint_common import PublicSourceClient, utc_now, write_json

try:
    import dns.resolver  # type: ignore
    HAS_DNS = True
except Exception:
    HAS_DNS = False


EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)
DISPOSABLE_HINTS = {"mailinator.com", "10minutemail.com", "guerrillamail.com", "tempmail.com", "yopmail.com"}


@dataclass
class EmailIntelResult:
    email: str
    valid_syntax: bool
    domain: str = ""
    local_part_sha256: str = ""
    mx_records: list[str] = field(default_factory=list)
    txt_records: list[str] = field(default_factory=list)
    disposable_hint: bool = False
    gravatar: dict[str, Any] = field(default_factory=dict)
    search_pivots: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    analysed_at_utc: str = field(default_factory=utc_now)


class EmailIntel:
    def __init__(self):
        self.http = PublicSourceClient(min_interval_seconds=1.0)

    def analyse(self, email: str) -> dict[str, Any]:
        email_norm = email.strip().lower()
        valid = bool(EMAIL_RE.match(email_norm))
        domain = email_norm.split("@", 1)[1] if "@" in email_norm else ""
        result = EmailIntelResult(
            email=email_norm,
            valid_syntax=valid,
            domain=domain,
            local_part_sha256=hashlib.sha256(email_norm.split("@", 1)[0].encode()).hexdigest() if "@" in email_norm else "",
            disposable_hint=domain in DISPOSABLE_HINTS,
            search_pivots=self.search_pivots(email_norm),
        )
        if valid and domain:
            result.mx_records = self._dns(domain, "MX")
            result.txt_records = self._dns(domain, "TXT")
            result.gravatar = self._gravatar(email_norm)
        return asdict(result)

    @staticmethod
    def search_pivots(email: str) -> list[str]:
        domain = email.split("@", 1)[1] if "@" in email else ""
        return [
            f'"{email}"',
            f'"{email}" "contact" OR "profile"',
            f'"{domain}" "privacy" "contact"' if domain else "",
            f'"{domain}" "security.txt"' if domain else "",
        ]

    @staticmethod
    def _dns(domain: str, rtype: str) -> list[str]:
        if not HAS_DNS:
            return []
        try:
            return [str(r) for r in dns.resolver.resolve(domain, rtype)]  # type: ignore[name-defined]
        except Exception:
            return []

    def _gravatar(self, email: str) -> dict[str, Any]:
        md5 = hashlib.md5(email.encode("utf-8")).hexdigest()  # noqa: S324 - Gravatar public hash convention
        url = f"https://www.gravatar.com/{md5}.json"
        resp = self.http.get(url, cache_ttl_seconds=86400)
        if resp.get("status_code") == 200:
            try:
                return {"exists": True, "hash": md5, "profile": json.loads(resp.get("text", "{}"))}
            except json.JSONDecodeError:
                return {"exists": True, "hash": md5, "profile": {}}
        return {"exists": False, "hash": md5}


def main() -> None:
    parser = argparse.ArgumentParser(description="Low-intrusion email OSINT checks")
    parser.add_argument("email")
    parser.add_argument("--out")
    args = parser.parse_args()
    data = EmailIntel().analyse(args.email)
    if args.out:
        write_json(args.out, data)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
