#!/usr/bin/env python3
"""
ospo :: data normaliser

Converts supported OSINT JSON outputs into a deterministic POLE-like graph:
entities, events, relationships, evidence references, and ingestion reporting.

The graph contains research leads. Matching labels across sources does not prove
that two records refer to the same real-world person, organisation, or object.
"""

from __future__ import annotations

import argparse
import math
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from osint_common import read_json, utc_now, write_json

JsonDict = dict[str, Any]
EntityType = Literal[
    "person",
    "organisation",
    "object",
    "location",
    "document",
    "url",
    "search_query",
    "archive_capture",
    "entity",
]
EventType = Literal[
    "event",
    "communication",
    "movement",
    "financial",
    "meeting",
    "incident",
    "document_event",
    "other",
]

SCHEMA_VERSION = "1.0"
ENTITY_NAMESPACE = uuid.UUID("8de46d51-a789-4f9c-9a1f-badc1a6f5031")
EVENT_NAMESPACE = uuid.UUID("631d626c-eaa6-44aa-a53c-60b5a7e3e558")

IDENTITY_PRIORITY = (
    "lei",
    "company_number",
    "identifier",
    "url",
    "domain",
    "email",
    "phone",
)

VALID_ENTITY_TYPES = frozenset(
    {
        "person",
        "organisation",
        "object",
        "location",
        "document",
        "url",
        "search_query",
        "archive_capture",
        "entity",
    }
)
VALID_EVENT_TYPES = frozenset(
    {
        "event",
        "communication",
        "movement",
        "financial",
        "meeting",
        "incident",
        "document_event",
        "other",
    }
)


class NormalisationError(ValueError):
    """Raised when input data cannot safely be normalized."""


@dataclass
class Provenance:
    """Minimal source attribution for graph material."""

    source: str
    evidence_ref: str = ""


@dataclass
class NormalisedEntity:
    """A POLE-like graph entity with stable identity and source provenance."""

    entity_id: str
    entity_type: EntityType
    label: str
    identifiers: JsonDict = field(default_factory=dict)
    attributes: JsonDict = field(default_factory=dict)
    provenance: list[Provenance] = field(default_factory=list)


@dataclass
class NormalisedEvent:
    """A dated or undated occurrence represented separately from entities."""

    event_id: str
    event_type: EventType
    label: str
    occurred_at_utc: str = ""
    original_datetime: str = ""
    attributes: JsonDict = field(default_factory=dict)
    provenance: list[Provenance] = field(default_factory=list)


@dataclass
class NormalisedEdge:
    """A directed, attributable relationship between graph nodes."""

    source: str
    target: str
    relationship: str
    confidence: float = 0.7
    evidence_ref: str = ""
    attributes: JsonDict = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)


@dataclass
class IngestionResult:
    """One file's normalization outcome."""

    path: str
    adapter: str | None
    status: Literal["ingested", "skipped", "failed"]
    entities_added: int = 0
    events_added: int = 0
    edges_added: int = 0
    message: str = ""


def _clean_text(value: Any, field_name: str, *, required: bool = False) -> str:
    """Validate and normalize a textual input."""
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise NormalisationError(f"{field_name} must be a string.")

    cleaned = " ".join(value.split())
    if required and not cleaned:
        raise NormalisationError(f"{field_name} must not be empty.")
    return cleaned


def _json_object(value: Any, field_name: str) -> JsonDict:
    """Copy a JSON-like mapping into a standard dictionary."""
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise NormalisationError(f"{field_name} must be an object.")
    return dict(value)


def _safe_value(value: Any) -> Any:
    """Return recursively JSON-serializable values only."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {
            str(key): _safe_value(item)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_safe_value(item) for item in value]
    return str(value)


def _nonempty_attributes(attributes: Mapping[str, Any]) -> JsonDict:
    """Keep meaningful, JSON-safe attribute values."""
    return {
        str(key): _safe_value(value)
        for key, value in attributes.items()
        if value not in (None, "", [], {})
    }


def _canonical_identifier(name: str, value: Any) -> str:
    """Create a deterministic comparison representation for an identifier."""
    normalized_name = _clean_text(name, "identifier name", required=True).casefold()
    normalized_value = _clean_text(
        str(value),
        f"identifier {name}",
        required=True,
    ).casefold()
    return f"{normalized_name}={normalized_value}"


def _canonical_identity(
    entity_type: str,
    label: str,
    identifiers: Mapping[str, Any],
) -> str:
    """Build a deterministic identity key using preferred stable identifiers."""
    for identifier_name in IDENTITY_PRIORITY:
        value = identifiers.get(identifier_name)
        if value not in (None, "", [], {}):
            return (
                f"{entity_type}|"
                f"{_canonical_identifier(identifier_name, value)}"
            )

    return f"{entity_type}|label={label.casefold()}"


def _merge_provenance(
    existing: list[Provenance],
    source: str,
    evidence_ref: str,
) -> None:
    """Append unique source/evidence provenance while preserving order."""
    candidate = Provenance(source=source, evidence_ref=evidence_ref)
    if candidate not in existing:
        existing.append(candidate)


class DataNormaliser:
    """Build a validated, deterministic POLE-like entity/event/edge graph."""

    def __init__(self) -> None:
        self.entities: dict[str, NormalisedEntity] = {}
        self.events: dict[str, NormalisedEvent] = {}
        self.edges: dict[tuple[str, str, str, str], NormalisedEdge] = {}
        self.identifier_conflicts: list[JsonDict] = []

    def add_entity(
        self,
        entity_type: EntityType,
        label: str,
        identifiers: Mapping[str, Any] | None = None,
        *,
        source: str = "",
        evidence_ref: str = "",
        attributes: Mapping[str, Any] | None = None,
    ) -> str:
        """Add or merge an entity and return its deterministic graph identifier."""
        if entity_type not in VALID_ENTITY_TYPES:
            raise NormalisationError(f"Unsupported entity type: {entity_type!r}")

        normalized_label = _clean_text(label, "entity label", required=True)
        normalized_identifiers = _nonempty_attributes(
            _json_object(identifiers, "identifiers")
        )
        normalized_attributes = _nonempty_attributes(
            _json_object(attributes, "attributes")
        )
        normalized_source = _clean_text(source, "source")
        normalized_evidence = _clean_text(evidence_ref, "evidence_ref")

        identity = _canonical_identity(
            entity_type,
            normalized_label,
            normalized_identifiers,
        )
        entity_id = f"ent_{uuid.uuid5(ENTITY_NAMESPACE, identity).hex}"

        existing = self.entities.get(entity_id)
        if existing is None:
            entity = NormalisedEntity(
                entity_id=entity_id,
                entity_type=entity_type,
                label=normalized_label,
                identifiers=normalized_identifiers,
                attributes=normalized_attributes,
            )
            if normalized_source:
                _merge_provenance(
                    entity.provenance,
                    normalized_source,
                    normalized_evidence,
                )
            self.entities[entity_id] = entity
            return entity_id

        for key, value in normalized_identifiers.items():
            old_value = existing.identifiers.get(key)
            if old_value in (None, "", [], {}):
                existing.identifiers[key] = value
            elif old_value != value:
                self.identifier_conflicts.append(
                    {
                        "entity_id": entity_id,
                        "identifier": key,
                        "existing_value": old_value,
                        "incoming_value": value,
                        "source": normalized_source,
                    }
                )

        for key, value in normalized_attributes.items():
            if key not in existing.attributes:
                existing.attributes[key] = value
            elif existing.attributes[key] != value:
                conflicts = existing.attributes.setdefault("_attribute_conflicts", {})
                if isinstance(conflicts, dict):
                    values = conflicts.setdefault(key, [])
                    if isinstance(values, list) and value not in values:
                        values.append(value)

        if normalized_source:
            _merge_provenance(
                existing.provenance,
                normalized_source,
                normalized_evidence,
            )
        return entity_id

    def add_event(
        self,
        event_type: EventType,
        label: str,
        *,
        occurred_at_utc: str = "",
        original_datetime: str = "",
        source: str = "",
        evidence_ref: str = "",
        attributes: Mapping[str, Any] | None = None,
    ) -> str:
        """Add or merge a deterministic event and return its graph identifier."""
        if event_type not in VALID_EVENT_TYPES:
            raise NormalisationError(f"Unsupported event type: {event_type!r}")

        normalized_label = _clean_text(label, "event label", required=True)
        normalized_time = _clean_text(occurred_at_utc, "occurred_at_utc")
        normalized_original = _clean_text(original_datetime, "original_datetime")
        normalized_source = _clean_text(source, "source")
        normalized_evidence = _clean_text(evidence_ref, "evidence_ref")
        normalized_attributes = _nonempty_attributes(
            _json_object(attributes, "event attributes")
        )

        identity = "|".join(
            (
                event_type,
                normalized_label.casefold(),
                normalized_time,
                normalized_original,
                normalized_evidence,
            )
        )
        event_id = f"evt_{uuid.uuid5(EVENT_NAMESPACE, identity).hex}"

        event = self.events.get(event_id)
        if event is None:
            event = NormalisedEvent(
                event_id=event_id,
                event_type=event_type,
                label=normalized_label,
                occurred_at_utc=normalized_time,
                original_datetime=normalized_original,
                attributes=normalized_attributes,
            )
            self.events[event_id] = event
        else:
            event.attributes.update(
                {
                    key: value
                    for key, value in normalized_attributes.items()
                    if key not in event.attributes
                }
            )

        if normalized_source:
            _merge_provenance(
                event.provenance,
                normalized_source,
                normalized_evidence,
            )
        return event_id

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        *,
        confidence: float = 0.7,
        evidence_ref: str = "",
        source: str = "",
        attributes: Mapping[str, Any] | None = None,
    ) -> None:
        """Add or merge an edge, rejecting dangling endpoints and invalid confidence."""
        if source_id not in self.nodes:
            raise NormalisationError(f"Unknown source node ID: {source_id}")
        if target_id not in self.nodes:
            raise NormalisationError(f"Unknown target node ID: {target_id}")

        normalized_relationship = _clean_text(
            relationship,
            "relationship",
            required=True,
        ).casefold()
        normalized_evidence = _clean_text(evidence_ref, "evidence_ref")
        normalized_source = _clean_text(source, "source")

        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise NormalisationError("confidence must be a number from 0.0 to 1.0.")
        if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
            raise NormalisationError("confidence must be a finite value from 0.0 to 1.0.")

        edge_key = (
            source_id,
            target_id,
            normalized_relationship,
            normalized_evidence,
        )
        edge = self.edges.get(edge_key)
        if edge is None:
            edge = NormalisedEdge(
                source=source_id,
                target=target_id,
                relationship=normalized_relationship,
                confidence=float(confidence),
                evidence_ref=normalized_evidence,
                attributes=_nonempty_attributes(
                    _json_object(attributes, "edge attributes")
                ),
                sources=[normalized_source] if normalized_source else [],
            )
            self.edges[edge_key] = edge
            return

        edge.confidence = max(edge.confidence, float(confidence))
        for key, value in _nonempty_attributes(
            _json_object(attributes, "edge attributes")
        ).items():
            edge.attributes.setdefault(key, value)
        if normalized_source and normalized_source not in edge.sources:
            edge.sources.append(normalized_source)

    @property
    def nodes(self) -> set[str]:
        """Return all valid graph node identifiers."""
        return set(self.entities) | set(self.events)

    def ingest_search_results(self, data: Mapping[str, Any]) -> None:
        """Ingest search-intelligence output containing engines and hit records."""
        hits = data.get("hits")
        if not isinstance(hits, list):
            raise NormalisationError("search results require a 'hits' array.")

        for index, hit in enumerate(hits, start=1):
            if not isinstance(hit, Mapping):
                raise NormalisationError(f"search hit {index} must be an object.")

            url = _clean_text(hit.get("url", ""), f"search hit {index} URL")
            title = _clean_text(hit.get("title", ""), f"search hit {index} title")
            label = title or url
            if not label:
                raise NormalisationError(
                    f"search hit {index} requires at least title or URL."
                )

            source = _clean_text(hit.get("engine", "search"), "search engine")
            document_id = self.add_entity(
                "document",
                label,
                {"url": url} if url else {},
                source=source or "search",
                attributes={"snippet": hit.get("snippet", "")},
            )

            query = _clean_text(hit.get("query", ""), "search query")
            if query:
                query_id = self.add_entity(
                    "search_query",
                    query,
                    source="search_intel",
                )
                raw_score = hit.get("score", 0.5)
                confidence = (
                    float(raw_score)
                    if isinstance(raw_score, (int, float))
                    and not isinstance(raw_score, bool)
                    and 0.0 <= float(raw_score) <= 1.0
                    else 0.5
                )
                self.add_edge(
                    query_id,
                    document_id,
                    "returned",
                    confidence=confidence,
                    source=source or "search",
                )

    def ingest_public_records(self, data: Mapping[str, Any]) -> None:
        """Ingest generic public-record search results."""
        hits = data.get("hits")
        if not isinstance(hits, list):
            raise NormalisationError("public records require a 'hits' array.")

        query = _clean_text(data.get("query", ""), "public-record query")
        query_id = self.add_entity(
            "search_query",
            query or "public_records_query",
            source="public_records",
        )

        document_sources = {"openalex", "crossref", "courtlistener"}
        for index, hit in enumerate(hits, start=1):
            if not isinstance(hit, Mapping):
                raise NormalisationError(
                    f"public-record hit {index} must be an object."
                )

            source = _clean_text(hit.get("source", "public_records"), "record source")
            title = _clean_text(hit.get("title", ""), "record title")
            identifier = _clean_text(hit.get("identifier", ""), "record identifier")
            url = _clean_text(hit.get("url", ""), "record URL")
            label = title or identifier or url

            if not label:
                raise NormalisationError(
                    f"public-record hit {index} needs title, identifier, or URL."
                )

            entity_type: EntityType = (
                "document"
                if source.casefold() in document_sources
                else "entity"
            )
            identifiers = {
                key: value
                for key, value in {
                    "identifier": identifier,
                    "url": url,
                }.items()
                if value
            }
            item_id = self.add_entity(
                entity_type,
                label,
                identifiers,
                source=source or "public_records",
                attributes={"summary": hit.get("summary", "")},
            )
            self.add_edge(
                query_id,
                item_id,
                "matched_public_record",
                confidence=0.65,
                source=source or "public_records",
            )

    def ingest_archive(self, data: Mapping[str, Any]) -> None:
        """Ingest an archive-intelligence response with Wayback captures."""
        requested_url = _clean_text(data.get("url", ""), "archive URL", required=True)
        url_id = self.add_entity(
            "url",
            requested_url,
            {"url": requested_url},
            source="archive_intel",
        )

        wayback = data.get("wayback")
        if not isinstance(wayback, list):
            raise NormalisationError("archive result requires a 'wayback' array.")

        for index, capture in enumerate(wayback, start=1):
            if not isinstance(capture, Mapping):
                raise NormalisationError(
                    f"Wayback capture {index} must be an object."
                )

            archive_url = _clean_text(
                capture.get("archive_url", ""),
                f"Wayback capture {index} archive_url",
                required=True,
            )
            timestamp = _clean_text(
                capture.get("timestamp", ""),
                f"Wayback capture {index} timestamp",
            )
            digest = _clean_text(
                capture.get("digest", ""),
                f"Wayback capture {index} digest",
            )

            capture_id = self.add_entity(
                "archive_capture",
                archive_url,
                {
                    key: value
                    for key, value in {
                        "url": archive_url,
                        "timestamp": timestamp,
                        "digest": digest,
                    }.items()
                    if value
                },
                source="wayback_cdx",
                attributes={
                    "status_code": capture.get("status_code"),
                    "mime_type": capture.get("mime_type"),
                },
            )
            self.add_edge(
                url_id,
                capture_id,
                "archived_as",
                confidence=0.9,
                evidence_ref=archive_url,
                source="wayback_cdx",
            )

    def to_graph_json(self) -> JsonDict:
        """Return deterministic graph JSON plus ingestion-quality signals."""
        entities = sorted(
            (asdict(entity) for entity in self.entities.values()),
            key=lambda entity: entity["entity_id"],
        )
        events = sorted(
            (asdict(event) for event in self.events.values()),
            key=lambda event: event["event_id"],
        )
        edges = sorted(
            (asdict(edge) for edge in self.edges.values()),
            key=lambda edge: (
                edge["source"],
                edge["relationship"],
                edge["target"],
                edge["evidence_ref"],
            ),
        )

        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": utc_now(),
            "interpretation_notice": (
                "Graph links are source-attributed research leads. Shared labels "
                "or identifiers must be analyst-verified before treating records "
                "as the same real-world entity."
            ),
            "entities": entities,
            "events": events,
            "edges": edges,
            "quality": {
                "identifier_conflicts": sorted(
                    self.identifier_conflicts,
                    key=lambda item: (
                        item["entity_id"],
                        item["identifier"],
                        str(item["incoming_value"]),
                    ),
                ),
            },
            "counts": {
                "entities": len(entities),
                "events": len(events),
                "edges": len(edges),
            },
        }


def _select_adapter(data: Mapping[str, Any]) -> tuple[str, str]:
    """Select an adapter only from stable, validated document-shape markers."""
    if isinstance(data.get("wayback"), list) and "url" in data:
        return "archive", "ingest_archive"

    if isinstance(data.get("hits"), list) and "engines" in data:
        return "search_results", "ingest_search_results"

    if isinstance(data.get("hits"), list) and "query" in data:
        return "public_records", "ingest_public_records"

    raise NormalisationError(
        "Unsupported JSON shape. Expected archive data ('url' plus 'wayback'), "
        "search data ('engines' plus 'hits'), or public records ('query' plus 'hits')."
    )


def normalise_files(paths: Sequence[str | Path], out: str | Path) -> JsonDict:
    """Normalize supported JSON files and return graph plus ingestion report."""
    if not paths:
        raise NormalisationError("At least one input JSON file is required.")

    normaliser = DataNormaliser()
    report: list[IngestionResult] = []

    for raw_path in paths:
        path = Path(raw_path)
        before = (
            len(normaliser.entities),
            len(normaliser.events),
            len(normaliser.edges),
        )

        try:
            data = read_json(path)
            if not isinstance(data, Mapping):
                raise NormalisationError("Root JSON value must be an object.")

            adapter_name, method_name = _select_adapter(data)
            method = getattr(normaliser, method_name)
            method(data)
        except (OSError, ValueError, TypeError, NormalisationError) as exc:
            report.append(
                IngestionResult(
                    path=str(path),
                    adapter=None,
                    status="failed",
                    message=str(exc),
                )
            )
            continue

        after = (
            len(normaliser.entities),
            len(normaliser.events),
            len(normaliser.edges),
        )
        report.append(
            IngestionResult(
                path=str(path),
                adapter=adapter_name,
                status="ingested",
                entities_added=after[0] - before[0],
                events_added=after[1] - before[1],
                edges_added=after[2] - before[2],
            )
        )

    graph = normaliser.to_graph_json()
    graph["ingestion"] = {
        "files": [asdict(item) for item in report],
        "ingested_files": sum(item.status == "ingested" for item in report),
        "failed_files": sum(item.status == "failed" for item in report),
    }

    write_json(out, graph)
    return graph


def main() -> int:
    """Run JSON-file normalization from the command line."""
    parser = argparse.ArgumentParser(
        description="Normalize OSINT JSON outputs into deterministic graph JSON"
    )
    parser.add_argument("json_files", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=Path("normalised_graph.json"))
    args = parser.parse_args()

    try:
        graph = normalise_files(args.json_files, args.out)
    except NormalisationError as exc:
        print(f"Normalization failed: {exc}", file=sys.stderr)
        return 2

    ingestion = graph["ingestion"]
    print(
        f"Graph: {graph['counts']['entities']} entities, "
        f"{graph['counts']['events']} events, "
        f"{graph['counts']['edges']} edges; "
        f"{ingestion['ingested_files']} files ingested, "
        f"{ingestion['failed_files']} files failed"
    )
    return 1 if ingestion["failed_files"] else 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())