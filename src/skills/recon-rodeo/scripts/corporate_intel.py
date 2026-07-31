#!/usr/bin/env python3
"""
ospo :: corporate intelligence aggregator

Cross-jurisdictional company research for UK Companies House, SEC EDGAR,
GLEIF LEI reference data, and ICIJ Offshore Leaks reconciliation.

Search results are leads requiring analyst verification. A source match does not
establish identity, control, ownership, misconduct, or legal liability.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

try:
    import requests
    from requests import Response, Session
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

JsonDict = dict[str, Any]
SourceStatus = Literal[
    "success",
    "not_configured",
    "unavailable",
    "failed",
    "skipped",
]

DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_LIMIT = 5
MAX_LIMIT = 20
MAX_QUERY_LENGTH = 256
MAX_RAW_RECORDS = 20

SEC_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions"
COMPANIES_HOUSE_URL = "https://api.company-information.service.gov.uk"
GLEIF_URL = "https://api.gleif.org/api/v1"
ICIJ_RECONCILIATION_URL = "https://offshoreleaks.icij.org/api/v1/reconcile"


class CorporateIntelError(RuntimeError):
    """Raised for invalid research input or unavailable required dependencies."""


class SourceRequestError(CorporateIntelError):
    """Raised when an external corporate-data source cannot be queried."""


@dataclass
class CompanyRecord:
    """Normalized lead from a single public corporate-data source."""

    source: str
    name: str
    jurisdiction: str = ""
    company_number: str = ""
    status: str = ""
    incorporation_date: str = ""
    address: str = ""
    officers: list[JsonDict] = field(default_factory=list)
    persons_with_significant_control: list[JsonDict] = field(default_factory=list)
    sic_codes: list[str] = field(default_factory=list)
    lei: str = ""
    parent_entity: str = ""
    raw_data: JsonDict = field(default_factory=dict)
    match_note: str = ""


@dataclass
class SourceResult:
    """A source-specific result whose status cannot be confused with no match."""

    source: str
    status: SourceStatus
    records: list[CompanyRecord] = field(default_factory=list)
    queried_at_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )
    error: str | None = None
    http_status: int | None = None
    warnings: list[str] = field(default_factory=list)


def utc_now() -> str:
    """Return a canonical UTC timestamp."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_query(query: str) -> str:
    """Validate and normalize a bounded company research query."""
    if not isinstance(query, str):
        raise CorporateIntelError("query must be a string.")

    normalized = " ".join(query.split())
    if not normalized:
        raise CorporateIntelError("query must not be empty.")
    if len(normalized) > MAX_QUERY_LENGTH:
        raise CorporateIntelError(
            f"query must not exceed {MAX_QUERY_LENGTH} characters."
        )
    return normalized


def validate_limit(limit: int) -> int:
    """Validate per-source result limit."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise CorporateIntelError("limit must be an integer.")
    if not 1 <= limit <= MAX_LIMIT:
        raise CorporateIntelError(f"limit must be between 1 and {MAX_LIMIT}.")
    return limit


def _safe_json(response: Response, *, source: str) -> JsonDict:
    """Parse a JSON object or raise a source-specific error."""
    try:
        data = response.json()
    except ValueError as exc:
        raise SourceRequestError(f"{source} returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise SourceRequestError(f"{source} returned a non-object JSON response.")
    return data


def _as_list(value: Any) -> list[Any]:
    """Return a list when value is a list; otherwise return an empty list."""
    return value if isinstance(value, list) else []


def _address_text(address: Any) -> str:
    """Normalize common API address structures into a compact display value."""
    if isinstance(address, str):
        return address.strip()
    if not isinstance(address, dict):
        return ""

    values: list[str] = []
    for key in (
        "address_line_1",
        "address_line_2",
        "addressLines",
        "locality",
        "city",
        "region",
        "postal_code",
        "postalCode",
        "country",
    ):
        value = address.get(key)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
        elif isinstance(value, list):
            values.extend(
                part.strip()
                for part in value
                if isinstance(part, str) and part.strip()
            )

    return ", ".join(dict.fromkeys(values))


def _atomic_write_json(path: Path, payload: JsonDict) -> None:
    """Atomically write a UTF-8 JSON document."""
    import tempfile

    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, indent=2, sort_keys=True) + "\n"

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary_path = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())

    try:
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


class PublicRegistryClient:
    """Shared HTTP client with bounded retries for public registry APIs."""

    def __init__(
        self,
        *,
        user_agent: str,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        if not HAS_REQUESTS:
            raise CorporateIntelError(
                "The 'requests' dependency is required for corporate research."
            )

        self.timeout_seconds = timeout_seconds
        self.session: Session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": user_agent,
            }
        )

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            status=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST"}),
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=4, pool_maxsize=4)
        self.session.mount("https://", adapter)

    def get(
        self,
        url: str,
        *,
        params: JsonDict | None = None,
        auth: tuple[str, str] | None = None,
    ) -> Response:
        """Perform a bounded GET and raise on unsuccessful HTTP status."""
        try:
            response = self.session.get(
                url,
                params=params,
                auth=auth,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise SourceRequestError(f"GET request failed: {exc}") from exc

        if not response.ok:
            raise SourceRequestError(
                f"GET request failed with HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )
        return response

    def post(
        self,
        url: str,
        *,
        data: JsonDict,
    ) -> Response:
        """Perform a bounded form-encoded POST and raise on bad status."""
        try:
            response = self.session.post(
                url,
                data=data,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise SourceRequestError(f"POST request failed: {exc}") from exc

        if not response.ok:
            raise SourceRequestError(
                f"POST request failed with HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )
        return response


class CompaniesHouse:
    """UK Companies House API client."""

    def __init__(self, client: PublicRegistryClient, api_key: str) -> None:
        self.client = client
        self.api_key = api_key

    @property
    def _auth(self) -> tuple[str, str]:
        return self.api_key, ""

    def search(self, query: str, limit: int) -> list[CompanyRecord]:
        """Search UK company records."""
        response = self.client.get(
            f"{COMPANIES_HOUSE_URL}/search/companies",
            params={"q": query, "items_per_page": limit},
            auth=self._auth,
        )
        data = _safe_json(response, source="Companies House")
        records: list[CompanyRecord] = []

        for item in _as_list(data.get("items"))[:limit]:
            if not isinstance(item, dict):
                continue

            records.append(
                CompanyRecord(
                    source="companies_house",
                    name=str(item.get("title", "")),
                    jurisdiction="GB",
                    company_number=str(item.get("company_number", "")),
                    status=str(item.get("company_status", "")),
                    incorporation_date=str(item.get("date_of_creation", "")),
                    address=str(item.get("address_snippet", "")),
                    sic_codes=[
                        str(code)
                        for code in _as_list(item.get("sic"))
                        if isinstance(code, (str, int))
                    ],
                    raw_data=item,
                )
            )

        return records

    def get_officers(self, company_number: str) -> list[JsonDict]:
        """Retrieve current and former officer appointments for a company."""
        response = self.client.get(
            f"{COMPANIES_HOUSE_URL}/company/{company_number}/officers",
            params={"items_per_page": 100},
            auth=self._auth,
        )
        data = _safe_json(response, source="Companies House officers")

        return [
            {
                "name": str(item.get("name", "")),
                "role": str(item.get("officer_role", "")),
                "appointed_on": str(item.get("appointed_on", "")),
                "resigned_on": str(item.get("resigned_on", "")),
                "nationality": str(item.get("nationality", "")),
                "country_of_residence": str(
                    item.get("country_of_residence", "")
                ),
            }
            for item in _as_list(data.get("items"))
            if isinstance(item, dict)
        ]

    def get_psc(self, company_number: str) -> list[JsonDict]:
        """Retrieve public Persons with Significant Control entries."""
        response = self.client.get(
            f"{COMPANIES_HOUSE_URL}/company/"
            f"{company_number}/persons-with-significant-control",
            params={"items_per_page": 100},
            auth=self._auth,
        )
        data = _safe_json(response, source="Companies House PSC")

        return [
            {
                "name": str(item.get("name", "")),
                "kind": str(item.get("kind", "")),
                "notified_on": str(item.get("notified_on", "")),
                "ceased_on": str(item.get("ceased_on", "")),
                "nationality": str(item.get("nationality", "")),
                "country_of_residence": str(
                    item.get("country_of_residence", "")
                ),
                "natures_of_control": [
                    str(control)
                    for control in _as_list(item.get("natures_of_control"))
                    if isinstance(control, str)
                ],
            }
            for item in _as_list(data.get("items"))
            if isinstance(item, dict)
        ]


class SECEdgar:
    """US SEC EDGAR company-identity and submission lookup client."""

    def __init__(self, client: PublicRegistryClient) -> None:
        self.client = client

    def search(self, query: str, limit: int) -> list[CompanyRecord]:
        """Search local SEC ticker/company mapping data by company name."""
        response = self.client.get(SEC_TICKERS_URL)
        ticker_map = _safe_json(response, source="SEC company tickers")
        query_key = query.casefold()

        matches: list[CompanyRecord] = []
        for entry in ticker_map.values():
            if not isinstance(entry, dict):
                continue

            title = str(entry.get("title", ""))
            ticker = str(entry.get("ticker", ""))
            if query_key not in title.casefold() and query_key != ticker.casefold():
                continue

            cik_value = entry.get("cik_str")
            try:
                cik = str(int(cik_value)).zfill(10)
            except (TypeError, ValueError):
                continue

            matches.append(
                CompanyRecord(
                    source="sec_edgar",
                    name=title,
                    jurisdiction="US",
                    company_number=cik,
                    raw_data=entry,
                    match_note=(
                        "Matched against the SEC company ticker/CIK reference file; "
                        "verify legal identity through filings."
                    ),
                )
            )

            if len(matches) >= limit:
                break

        return matches

    def get_submissions(self, cik: str) -> JsonDict:
        """Retrieve SEC filing submissions for one zero-padded CIK."""
        normalized_cik = str(int(cik)).zfill(10)
        response = self.client.get(
            f"{SEC_SUBMISSIONS_URL}/CIK{normalized_cik}.json"
        )
        return _safe_json(response, source="SEC submissions")


class GLEIF:
    """GLEIF LEI reference-data client."""

    def __init__(self, client: PublicRegistryClient) -> None:
        self.client = client

    def search(self, query: str, limit: int) -> list[CompanyRecord]:
        """Search global LEI records by legal-entity full text."""
        response = self.client.get(
            f"{GLEIF_URL}/lei-records",
            params={"filter[fulltext]": query, "page[size]": limit},
        )
        data = _safe_json(response, source="GLEIF")
        records: list[CompanyRecord] = []

        for item in _as_list(data.get("data"))[:limit]:
            if not isinstance(item, dict):
                continue

            attributes = item.get("attributes")
            if not isinstance(attributes, dict):
                continue

            entity = attributes.get("entity")
            if not isinstance(entity, dict):
                continue

            legal_name = entity.get("legalName")
            name = (
                str(legal_name.get("name", ""))
                if isinstance(legal_name, dict)
                else ""
            )

            records.append(
                CompanyRecord(
                    source="gleif",
                    name=name,
                    jurisdiction=str(entity.get("jurisdiction", "")),
                    status=str(entity.get("status", "")),
                    address=_address_text(entity.get("legalAddress")),
                    lei=str(item.get("id", "")),
                    raw_data=item,
                    match_note=(
                        "LEI reference-data match; use the LEI relationship "
                        "endpoints to assess reported parent relationships."
                    ),
                )
            )

        return records


class ICIJOffshoreLeaks:
    """ICIJ Offshore Leaks reconciliation client for lead generation."""

    def __init__(self, client: PublicRegistryClient) -> None:
        self.client = client

    def search(self, query: str, limit: int) -> list[CompanyRecord]:
        """Return potential ICIJ database matches, not findings of wrongdoing."""
        request_body = {
            "q0": {
                "query": query,
                "limit": limit,
            }
        }
        response = self.client.post(
            ICIJ_RECONCILIATION_URL,
            data={"queries": json.dumps(request_body)},
        )
        data = _safe_json(response, source="ICIJ Offshore Leaks")

        query_result = data.get("q0")
        if not isinstance(query_result, dict):
            raise SourceRequestError("ICIJ response did not contain query key 'q0'.")

        records: list[CompanyRecord] = []
        for item in _as_list(query_result.get("result"))[:limit]:
            if not isinstance(item, dict):
                continue

            records.append(
                CompanyRecord(
                    source="icij_offshore_leaks",
                    name=str(item.get("name", "")),
                    jurisdiction=str(item.get("jurisdiction", "")),
                    raw_data=item,
                    match_note=(
                        "Potential database match only. Verify identifiers, "
                        "jurisdiction, dates, and underlying ICIJ source context; "
                        "a match does not imply wrongdoing."
                    ),
                )
            )

        return records


class CorporateIntel:
    """Run bounded, source-attributed public corporate-record searches."""

    def __init__(
        self,
        *,
        ch_api_key: str | None = None,
        sec_user_agent: str | None = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        if not HAS_REQUESTS:
            raise CorporateIntelError(
                "Install requests to use CorporateIntel: pip install requests"
            )

        self.ch_api_key = ch_api_key or os.environ.get("CH_API_KEY")
        sec_identity = sec_user_agent or os.environ.get("SEC_USER_AGENT")

        if not sec_identity:
            raise CorporateIntelError(
                "SEC_USER_AGENT must identify the operator and provide a contact, "
                "for example 'Povvo Corporate Research contact@example.org'."
            )

        self.ch_client = PublicRegistryClient(
            user_agent="ospo-corporate-intel/1.0",
            timeout_seconds=timeout_seconds,
        )
        self.sec_client = PublicRegistryClient(
            user_agent=sec_identity,
            timeout_seconds=timeout_seconds,
        )
        self.public_client = PublicRegistryClient(
            user_agent="ospo-corporate-intel/1.0",
            timeout_seconds=timeout_seconds,
        )

        self.ch = (
            CompaniesHouse(self.ch_client, self.ch_api_key)
            if self.ch_api_key
            else None
        )
        self.edgar = SECEdgar(self.sec_client)
        self.gleif = GLEIF(self.public_client)
        self.icij = ICIJOffshoreLeaks(self.public_client)

    @staticmethod
    def _execute_source(
        source: str,
        search: Callable[[str, int], list[CompanyRecord]] | None,
        query: str,
        limit: int,
        *,
        unavailable_reason: str | None = None,
    ) -> SourceResult:
        """Run a source search without conflating no matches and source failures."""
        if search is None:
            return SourceResult(
                source=source,
                status="not_configured",
                warnings=[unavailable_reason or "Source is not configured."],
            )

        try:
            records = search(query, limit)
        except SourceRequestError as exc:
            return SourceResult(
                source=source,
                status="unavailable",
                error=str(exc),
            )
        except (TypeError, ValueError, KeyError) as exc:
            return SourceResult(
                source=source,
                status="failed",
                error=f"Unexpected source response shape: {exc}",
            )

        return SourceResult(
            source=source,
            status="success",
            records=records,
            warnings=(
                ["No matching records returned; this is not an identity clearance."]
                if not records
                else []
            ),
        )

    def _enrich_companies_house(
        self,
        source_result: SourceResult,
    ) -> SourceResult:
        """Attach officer and PSC lead data while retaining partial enrichment."""
        if self.ch is None or source_result.status != "success":
            return source_result

        warnings = list(source_result.warnings)
        for record in source_result.records:
            if not record.company_number:
                continue

            try:
                record.officers = self.ch.get_officers(record.company_number)
            except SourceRequestError as exc:
                warnings.append(
                    f"Officer lookup unavailable for {record.company_number}: {exc}"
                )

            try:
                record.persons_with_significant_control = self.ch.get_psc(
                    record.company_number
                )
            except SourceRequestError as exc:
                warnings.append(
                    f"PSC lookup unavailable for {record.company_number}: {exc}"
                )

            # Companies House permits 600 requests/5 minutes. This small delay
            # smooths enrichment bursts; HTTP retries handle actual 429 responses.
            time.sleep(0.1 + random.uniform(0.0, 0.05))

        source_result.warnings = warnings
        return source_result

    def investigate(self, query: str, *, limit: int = DEFAULT_LIMIT) -> JsonDict:
        """Search all configured sources and preserve each source's outcome."""
        normalized_query = validate_query(query)
        validated_limit = validate_limit(limit)

        companies_house = self._execute_source(
            "companies_house",
            self.ch.search if self.ch else None,
            normalized_query,
            validated_limit,
            unavailable_reason="CH_API_KEY is not set.",
        )
        companies_house = self._enrich_companies_house(companies_house)

        source_results = [
            companies_house,
            self._execute_source(
                "sec_edgar",
                self.edgar.search,
                normalized_query,
                validated_limit,
            ),
            self._execute_source(
                "gleif",
                self.gleif.search,
                normalized_query,
                validated_limit,
            ),
            self._execute_source(
                "icij_offshore_leaks",
                self.icij.search,
                normalized_query,
                validated_limit,
            ),
        ]

        return {
            "schema_version": "1.0",
            "query": normalized_query,
            "collected_at_utc": utc_now(),
            "limit_per_source": validated_limit,
            "interpretation_notice": (
                "Results are public-record search leads. Verify legal identity "
                "using stable identifiers and source documents before drawing "
                "conclusions. A source match does not establish beneficial "
                "ownership, control, misconduct, or legal liability."
            ),
            "sources": {
                result.source: {
                    "status": result.status,
                    "queried_at_utc": result.queried_at_utc,
                    "record_count": len(result.records),
                    "records": [asdict(record) for record in result.records],
                    "error": result.error,
                    "warnings": result.warnings,
                }
                for result in source_results
            },
        }


def main() -> int:
    """Run corporate research from the command line."""
    parser = argparse.ArgumentParser(
        description="Cross-jurisdictional public corporate-record research"
    )
    parser.add_argument("query", help="Company name, ticker, LEI, or identifier")
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum results per source (1-{MAX_LIMIT})",
    )
    parser.add_argument(
        "--sec-user-agent",
        help=(
            "Identifying SEC User-Agent with a contact address. "
            "Defaults to SEC_USER_AGENT."
        ),
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write the JSON report atomically to this path",
    )
    args = parser.parse_args()

    try:
        investigator = CorporateIntel(sec_user_agent=args.sec_user_agent)
        report = investigator.investigate(args.query, limit=args.limit)
    except CorporateIntelError as exc:
        print(f"Corporate research failed: {exc}", file=sys.stderr)
        return 2

    if args.output is not None:
        _atomic_write_json(args.output, report)
        print(f"Results written to {args.output}")
    else:
        print(json.dumps(report, indent=2, sort_keys=True))

    unavailable = sum(
        1
        for source in report["sources"].values()
        if source["status"] in {"unavailable", "failed"}
    )
    return 1 if unavailable else 0


if __name__ == "__main__":
    raise SystemExit(main())
