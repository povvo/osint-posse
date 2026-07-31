#!/usr/bin/env python3
"""
ospo :: source registry
Machine-readable catalogue of public-source APIs, datasets, and tooling surfaces.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from osint_common import write_json


@dataclass(frozen=True)
class SourceDefinition:
    source_id: str
    name: str
    category: str
    base_url: str
    auth: str = "none"
    cost: str = "free_or_limited_free"
    update_frequency: str = "unknown"
    licence: str = "check_source_terms"
    typical_entities: tuple[str, ...] = ()
    use_for: tuple[str, ...] = ()
    notes: str = ""
    passive_only: bool = True


SOURCES: tuple[SourceDefinition, ...] = (
    SourceDefinition("exa", "Exa Search", "search", "https://api.exa.ai", "EXA_API_KEY", typical_entities=("url", "document", "organisation"), use_for=("semantic discovery", "source finding", "content extraction")),
    SourceDefinition("tavily", "Tavily", "search", "https://api.tavily.com", "TAVILY_API_KEY", typical_entities=("url", "document"), use_for=("search", "extract", "crawl", "map", "research")),
    SourceDefinition("gdelt_doc", "GDELT DOC 2.0", "news_media", "https://api.gdeltproject.org/api/v2/doc/doc", "none", update_frequency="near-real-time", typical_entities=("article", "domain", "organisation", "location"), use_for=("global news monitoring", "coverage timelines", "tone")),
    SourceDefinition("gdelt_cloud", "GDELT Cloud API v2", "news_events", "https://api.gdeltcloud.com/api/v2", "none_or_plan", update_frequency="near-real-time", typical_entities=("event", "story", "entity"), use_for=("structured events", "story clusters", "entity discovery")),
    SourceDefinition("wayback_cdx", "Internet Archive CDX", "archive", "https://web.archive.org/cdx", "none", typical_entities=("url", "domain"), use_for=("historical captures", "deleted-source recovery")),
    SourceDefinition("common_crawl_index", "Common Crawl Index", "archive", "https://index.commoncrawl.org", "none", typical_entities=("url", "domain"), use_for=("historical web text discovery", "bulk public web index lookup")),
    SourceDefinition("wikidata", "Wikidata SPARQL", "knowledge_graph", "https://query.wikidata.org/sparql", "none", typical_entities=("person", "organisation", "location", "event"), use_for=("structured entity facts", "aliases", "relationships")),
    SourceDefinition("wikipedia", "Wikipedia REST", "knowledge_graph", "https://en.wikipedia.org/api/rest_v1", "none", typical_entities=("person", "organisation", "event"), use_for=("narrative context", "citations")),
    SourceDefinition("openalex", "OpenAlex", "research", "https://api.openalex.org", "none", typical_entities=("work", "author", "institution"), use_for=("scholarly research intelligence", "publication networks")),
    SourceDefinition("crossref", "Crossref", "research", "https://api.crossref.org", "none", typical_entities=("work", "funder", "publisher"), use_for=("DOI lookup", "publication metadata")),
    SourceDefinition("courtlistener", "CourtListener", "legal", "https://www.courtlistener.com/api/rest/v4", "optional_token", typical_entities=("case", "opinion", "docket", "party"), use_for=("court records", "opinions", "dockets")),
    SourceDefinition("companies_house", "UK Companies House", "corporate", "https://api.company-information.service.gov.uk", "CH_API_KEY", typical_entities=("company", "officer", "psc"), use_for=("UK registry", "officers", "beneficial ownership")),
    SourceDefinition("opencorporates", "OpenCorporates", "corporate", "https://api.opencorporates.com", "OPENCORPORATES_API_TOKEN", typical_entities=("company", "officer", "filing"), use_for=("multi-jurisdiction company search", "filings", "officers")),
    SourceDefinition("sec_edgar", "SEC EDGAR", "corporate_financial", "https://data.sec.gov", "none", typical_entities=("company", "filing", "xbrl_fact"), use_for=("US filings", "company facts", "submissions")),
    SourceDefinition("gleif", "GLEIF LEI", "corporate", "https://api.gleif.org/api/v1", "none", typical_entities=("legal_entity", "lei"), use_for=("legal entity identifier resolution", "corporate identity")),
    SourceDefinition("opensanctions", "OpenSanctions", "compliance", "https://api.opensanctions.org", "optional_or_commercial", typical_entities=("person", "organisation"), use_for=("sanctions", "PEP", "risk screening")),
    SourceDefinition("ofac", "OFAC SDN CSV", "compliance", "https://www.treasury.gov/ofac/downloads/sdn.csv", "none", typical_entities=("person", "organisation"), use_for=("US sanctions screening")),
    SourceDefinition("uk_sanctions", "UK Sanctions List", "compliance", "https://www.gov.uk/government/publications/the-uk-sanctions-list", "none", typical_entities=("person", "organisation"), use_for=("UK sanctions screening")),
    SourceDefinition("rdap", "RDAP", "domain", "https://rdap.org", "none", typical_entities=("domain", "ip", "asn"), use_for=("registration data", "nameservers", "domain events")),
    SourceDefinition("crtsh", "crt.sh", "domain", "https://crt.sh", "none", typical_entities=("certificate", "subdomain"), use_for=("certificate transparency", "subdomain clues")),
    SourceDefinition("shodan_internetdb", "Shodan InternetDB", "domain_ip", "https://internetdb.shodan.io", "none", typical_entities=("ip", "port", "vulnerability"), use_for=("passive host enrichment", "exposure triage")),
    SourceDefinition("urlhaus", "URLhaus", "threat_reputation", "https://urlhaus-api.abuse.ch", "none", typical_entities=("url", "domain", "hash"), use_for=("malware URL reputation", "indicator triage")),
    SourceDefinition("alienvault_otx", "AlienVault OTX", "threat_reputation", "https://otx.alienvault.com/api/v1", "OTX_API_KEY", typical_entities=("ip", "domain", "url", "file_hash"), use_for=("indicator pulses", "passive enrichment")),
    SourceDefinition("overpass", "OpenStreetMap Overpass", "geospatial", "https://overpass-api.de/api/interpreter", "none", typical_entities=("place", "amenity", "road", "building"), use_for=("nearby features", "map context")),
    SourceDefinition("nominatim", "Nominatim", "geospatial", "https://nominatim.openstreetmap.org", "none", typical_entities=("address", "coordinate", "place"), use_for=("geocoding", "reverse geocoding")),
    SourceDefinition("open_meteo", "Open-Meteo", "geospatial", "https://api.open-meteo.com", "none", typical_entities=("weather", "coordinate"), use_for=("current weather", "historical weather")),
    SourceDefinition("blockstream", "Blockstream Bitcoin API", "blockchain", "https://blockstream.info/api", "none", typical_entities=("btc_address", "transaction"), use_for=("Bitcoin address and transaction context")),
    SourceDefinition("etherscan", "Etherscan", "blockchain", "https://api.etherscan.io/api", "ETHERSCAN_API_KEY", typical_entities=("eth_address", "transaction"), use_for=("Ethereum address and transaction context")),
)


def all_sources() -> list[dict]:
    return [asdict(s) for s in SOURCES]


def filter_sources(category: str | None = None, auth: str | None = None) -> list[dict]:
    rows = all_sources()
    if category:
        rows = [r for r in rows if r["category"] == category]
    if auth:
        rows = [r for r in rows if r["auth"] == auth]
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="List OSINT source definitions")
    parser.add_argument("--category")
    parser.add_argument("--auth")
    parser.add_argument("--out")
    args = parser.parse_args()
    rows = filter_sources(args.category, args.auth)
    if args.out:
        write_json(args.out, rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
