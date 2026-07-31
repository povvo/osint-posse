#!/usr/bin/env python3
"""
ospo :: phone intelligence
Phone number normalisation and non-intrusive context. Does not call or message numbers.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict, field

from osint_common import utc_now, write_json

try:
    import phonenumbers  # type: ignore
    from phonenumbers import carrier, geocoder, timezone  # type: ignore
    HAS_PHONENUMBERS = True
except Exception:
    HAS_PHONENUMBERS = False


@dataclass
class PhoneIntelResult:
    raw: str
    default_region: str
    possible: bool = False
    valid: bool = False
    e164: str = ""
    international: str = ""
    national: str = ""
    country_code: int | None = None
    region_code: str = ""
    carrier: str = ""
    geocoder_description: str = ""
    timezones: list[str] = field(default_factory=list)
    search_pivots: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    analysed_at_utc: str = field(default_factory=utc_now)


class PhoneIntel:
    def analyse(self, number: str, default_region: str = "GB") -> dict:
        result = PhoneIntelResult(raw=number, default_region=default_region)
        if not HAS_PHONENUMBERS:
            result.warnings.append("phonenumbers not installed")
            result.search_pivots = self.search_pivots(number)
            return asdict(result)
        try:
            parsed = phonenumbers.parse(number, default_region)  # type: ignore[name-defined]
            result.possible = phonenumbers.is_possible_number(parsed)  # type: ignore[name-defined]
            result.valid = phonenumbers.is_valid_number(parsed)  # type: ignore[name-defined]
            result.e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)  # type: ignore[name-defined]
            result.international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)  # type: ignore[name-defined]
            result.national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)  # type: ignore[name-defined]
            result.country_code = parsed.country_code
            result.region_code = phonenumbers.region_code_for_number(parsed) or ""  # type: ignore[name-defined]
            result.carrier = carrier.name_for_number(parsed, "en")  # type: ignore[name-defined]
            result.geocoder_description = geocoder.description_for_number(parsed, "en")  # type: ignore[name-defined]
            result.timezones = list(timezone.time_zones_for_number(parsed))  # type: ignore[name-defined]
            result.search_pivots = self.search_pivots(result.e164 or number)
        except Exception as exc:
            result.warnings.append(str(exc))
            result.search_pivots = self.search_pivots(number)
        return asdict(result)

    @staticmethod
    def search_pivots(number: str) -> list[str]:
        compact = number.replace(" ", "")
        return [f'"{number}"', f'"{compact}"', f'"{number}" "contact"', f'"{compact}" "WhatsApp"']


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse phone number format and public pivots")
    parser.add_argument("number")
    parser.add_argument("--region", default="GB")
    parser.add_argument("--out")
    args = parser.parse_args()
    data = PhoneIntel().analyse(args.number, args.region)
    if args.out:
        write_json(args.out, data)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
