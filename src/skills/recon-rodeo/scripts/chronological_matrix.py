#!/usr/bin/env python3
"""
ospo :: chronological matrix

UTC-normalized timeline construction with explicit time precision, gap
identification, correlation candidates, and temporal-discrepancy flagging.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
import tempfile
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATE_ONLY_FORMAT = "%Y-%m-%d"
EVENT_ID_RE = re.compile(r"^EVT-\d{4,}$")
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9'-]*")

DEFAULT_CATEGORY = "other"
VALID_CATEGORIES = frozenset(
    {
        "communication",
        "movement",
        "financial",
        "meeting",
        "incident",
        "document",
        "other",
    }
)
VALID_SOURCE_RELIABILITY = frozenset({"", "A", "B", "C", "D", "E", "F"})
VALID_INFORMATION_CREDIBILITY = frozenset({"", "1", "2", "3", "4", "5", "6"})

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "at",
        "by",
        "for",
        "from",
        "in",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
)

TimePrecision = Literal["date", "minute", "second"]
NaiveDatetimePolicy = Literal["reject", "utc", "assume_timezone"]


class ChronologyValidationError(ValueError):
    """Raised when an event or analysis option is invalid."""


@dataclass(frozen=True)
class ParsedTime:
    """A normalized timestamp together with source precision metadata."""

    original: str
    utc_datetime: datetime
    precision: TimePrecision
    timezone_assumption: str | None = None

    @property
    def utc_isoformat(self) -> str:
        """Return a canonical seconds-precision UTC ISO-8601 value."""
        return self.utc_datetime.isoformat(timespec="seconds")

    @property
    def uncertainty_seconds(self) -> int:
        """Return the maximum rounding uncertainty implied by source precision."""
        if self.precision == "date":
            return 86_400
        if self.precision == "minute":
            return 60
        return 1


@dataclass
class TimelineEvent:
    """One source-attributed event, normalized without discarding source time."""

    event_id: str
    original_datetime: str
    utc_datetime: str
    time_precision: TimePrecision
    timezone_assumption: str | None
    description: str
    source: str = ""
    source_reliability: str = ""
    info_credibility: str = ""
    entities_involved: list[str] = field(default_factory=list)
    location: str = ""
    category: str = DEFAULT_CATEGORY
    evidence_ref: str = ""
    notes: str = ""
    conflicts_with: list[str] = field(default_factory=list)


def _parse_naive_timezone(value: str | None) -> timezone:
    """Parse a fixed UTC offset such as '+01:00'; reject named zones."""
    if value is None:
        raise ChronologyValidationError(
            "A timezone offset is required when naive_datetime_policy="
            "'assume_timezone'."
        )

    normalized = value.strip().upper()
    if normalized == "Z":
        return timezone.utc

    match = re.fullmatch(r"([+-])(\d{2}):?(\d{2})", normalized)
    if match is None:
        raise ChronologyValidationError(
            "default_timezone must be 'Z', '+HH:MM', or '-HH:MM'. "
            "Named zones are intentionally not accepted."
        )

    sign, hours_text, minutes_text = match.groups()
    hours = int(hours_text)
    minutes = int(minutes_text)
    if hours > 23 or minutes > 59:
        raise ChronologyValidationError(f"Invalid UTC offset: {value!r}")

    offset = timedelta(hours=hours, minutes=minutes)
    return timezone(offset if sign == "+" else -offset)


def _detect_precision(value: str) -> TimePrecision:
    """Identify precision from an accepted ISO-8601 source representation."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return "date"
    if re.fullmatch(r".*[T ]\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})?", value):
        return "minute"
    return "second"


def parse_to_utc(
    dt_string: str,
    *,
    naive_datetime_policy: NaiveDatetimePolicy = "reject",
    default_timezone: str | None = None,
) -> ParsedTime:
    """Parse an ISO-8601 timestamp and normalize it to UTC.

    Accepted inputs are ISO-8601 date, minute, and second representations.
    Naive datetime values are rejected by default because their timezone is
    unknown. Date-only values represent a calendar day, not midnight evidence.
    """
    if not isinstance(dt_string, str) or not dt_string.strip():
        raise ChronologyValidationError("Event datetime must be a non-empty string.")

    source_value = dt_string.strip()
    normalized = (
        source_value[:-1] + "+00:00"
        if source_value.endswith(("Z", "z"))
        else source_value
    )

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ChronologyValidationError(
            "Datetime must be ISO-8601, for example "
            "'2025-06-15T14:30:00+01:00' or '2025-06-15'."
        ) from exc

    precision = _detect_precision(source_value)
    timezone_assumption: str | None = None

    if parsed.tzinfo is None:
        if naive_datetime_policy == "reject":
            raise ChronologyValidationError(
                "Naive datetime has no timezone. Supply an explicit offset, "
                "use 'Z', or configure a documented timezone policy."
            )
        if naive_datetime_policy == "utc":
            parsed = parsed.replace(tzinfo=timezone.utc)
            timezone_assumption = "assumed_utc"
        elif naive_datetime_policy == "assume_timezone":
            assumed_timezone = _parse_naive_timezone(default_timezone)
            parsed = parsed.replace(tzinfo=assumed_timezone)
            timezone_assumption = f"assumed_offset:{default_timezone}"
        else:
            raise ChronologyValidationError(
                f"Unsupported naive datetime policy: {naive_datetime_policy!r}"
            )

    return ParsedTime(
        original=source_value,
        utc_datetime=parsed.astimezone(timezone.utc),
        precision=precision,
        timezone_assumption=timezone_assumption,
    )


def _normalize_text(value: str, *, field_name: str) -> str:
    """Validate and trim a textual field."""
    if not isinstance(value, str):
        raise ChronologyValidationError(f"{field_name} must be a string.")
    return value.strip()


def _normalize_entities(entities: Iterable[str] | None) -> list[str]:
    """Validate, de-duplicate, and preserve first-seen entity ordering."""
    if entities is None:
        return []
    if isinstance(entities, (str, bytes)):
        raise ChronologyValidationError(
            "entities must be an iterable of strings, not a single string."
        )

    normalized: list[str] = []
    seen: set[str] = set()

    for entity in entities:
        cleaned = _normalize_text(entity, field_name="Each entity")
        if not cleaned:
            raise ChronologyValidationError("Entity names must not be empty.")

        key = cleaned.casefold()
        if key not in seen:
            seen.add(key)
            normalized.append(cleaned)

    return normalized


def _description_tokens(description: str) -> set[str]:
    """Extract meaningful normalized description tokens."""
    return {
        token
        for token in TOKEN_RE.findall(description.casefold())
        if token not in STOPWORDS and len(token) > 1
    }


def _csv_safe(value: Any) -> str:
    """Prevent spreadsheet applications treating exported data as a formula."""
    if isinstance(value, list):
        text = "; ".join(str(item) for item in value)
    else:
        text = str(value)

    return f"'{text}" if text.startswith(("=", "+", "-", "@")) else text


def _atomic_write_text(path: Path, content: str) -> None:
    """Atomically write UTF-8 text, avoiding partially written output files."""
    path.parent.mkdir(parents=True, exist_ok=True)

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

    try:
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)


class ChronologicalMatrix:
    """A UTC-normalized, source-attributed investigation timeline."""

    def __init__(
        self,
        *,
        naive_datetime_policy: NaiveDatetimePolicy = "reject",
        default_timezone: str | None = None,
    ) -> None:
        if naive_datetime_policy not in {
            "reject",
            "utc",
            "assume_timezone",
        }:
            raise ChronologyValidationError(
                "naive_datetime_policy must be 'reject', 'utc', or "
                "'assume_timezone'."
            )
        if (
            naive_datetime_policy == "assume_timezone"
            and default_timezone is None
        ):
            raise ChronologyValidationError(
                "default_timezone is required for 'assume_timezone'."
            )

        self.naive_datetime_policy = naive_datetime_policy
        self.default_timezone = default_timezone
        self.events: list[TimelineEvent] = []
        self._counter = 0

    def add_event(
        self,
        datetime_str: str,
        description: str,
        source: str = "",
        source_reliability: str = "",
        info_credibility: str = "",
        entities: Iterable[str] | None = None,
        location: str = "",
        category: str = DEFAULT_CATEGORY,
        evidence_ref: str = "",
        notes: str = "",
    ) -> str:
        """Add a validated source-attributed event and return its event ID."""
        parsed_time = parse_to_utc(
            datetime_str,
            naive_datetime_policy=self.naive_datetime_policy,
            default_timezone=self.default_timezone,
        )
        normalized_description = _normalize_text(description, field_name="description")
        if not normalized_description:
            raise ChronologyValidationError(
                "Event description must be a non-empty string."
            )

        normalized_category = _normalize_text(category, field_name="category").casefold()
        if normalized_category not in VALID_CATEGORIES:
            choices = ", ".join(sorted(VALID_CATEGORIES))
            raise ChronologyValidationError(
                f"Unknown category {category!r}; expected one of: {choices}."
            )

        normalized_reliability = _normalize_text(
            source_reliability,
            field_name="source_reliability",
        ).upper()
        if normalized_reliability not in VALID_SOURCE_RELIABILITY:
            raise ChronologyValidationError(
                "source_reliability must be blank or a letter from A to F."
            )

        normalized_credibility = _normalize_text(
            info_credibility,
            field_name="info_credibility",
        )
        if normalized_credibility not in VALID_INFORMATION_CREDIBILITY:
            raise ChronologyValidationError(
                "info_credibility must be blank or a number from 1 to 6."
            )

        self._counter += 1
        event_id = f"EVT-{self._counter:04d}"

        self.events.append(
            TimelineEvent(
                event_id=event_id,
                original_datetime=parsed_time.original,
                utc_datetime=parsed_time.utc_isoformat,
                time_precision=parsed_time.precision,
                timezone_assumption=parsed_time.timezone_assumption,
                description=normalized_description,
                source=_normalize_text(source, field_name="source"),
                source_reliability=normalized_reliability,
                info_credibility=normalized_credibility,
                entities_involved=_normalize_entities(entities),
                location=_normalize_text(location, field_name="location"),
                category=normalized_category,
                evidence_ref=_normalize_text(
                    evidence_ref,
                    field_name="evidence_ref",
                ),
                notes=_normalize_text(notes, field_name="notes"),
            )
        )
        return event_id

    def _sorted_events(self) -> list[TimelineEvent]:
        """Return a deterministic chronological view without mutating storage."""
        return sorted(
            self.events,
            key=lambda event: (event.utc_datetime, event.event_id),
        )

    @staticmethod
    def _event_datetime(event: TimelineEvent) -> datetime:
        """Parse an internally canonical UTC timestamp."""
        return datetime.fromisoformat(event.utc_datetime)

    @staticmethod
    def _validate_nonnegative_finite(value: float, *, field_name: str) -> float:
        """Validate a finite non-negative numeric analysis threshold."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ChronologyValidationError(f"{field_name} must be a number.")
        if not math.isfinite(value) or value < 0:
            raise ChronologyValidationError(
                f"{field_name} must be a finite non-negative number."
            )
        return float(value)

    def detect_gaps(self, min_gap_hours: float = 24.0) -> list[dict[str, Any]]:
        """Identify adjacent event gaps that exceed a stated threshold."""
        threshold_hours = self._validate_nonnegative_finite(
            min_gap_hours,
            field_name="min_gap_hours",
        )
        sorted_events = self._sorted_events()
        gaps: list[dict[str, Any]] = []

        for before, after in zip(sorted_events, sorted_events[1:], strict=True):
            duration = self._event_datetime(after) - self._event_datetime(before)
            duration_hours = duration.total_seconds() / 3600

            if duration_hours >= threshold_hours:
                gaps.append(
                    {
                        "gap_start": before.utc_datetime,
                        "gap_end": after.utc_datetime,
                        "duration_hours": round(duration_hours, 2),
                        "before_event": before.event_id,
                        "after_event": after.event_id,
                        "flag": "INTELLIGENCE_GAP",
                        "interpretation": (
                            "No events were supplied between these timestamps; "
                            "this is not evidence that no activity occurred."
                        ),
                    }
                )

        return gaps

    @staticmethod
    def _semantic_overlap(
        first: TimelineEvent,
        second: TimelineEvent,
    ) -> tuple[list[str], list[str]]:
        """Return shared meaningful words and shared named entities."""
        shared_tokens = sorted(
            _description_tokens(first.description)
            & _description_tokens(second.description)
        )
        first_entities = {entity.casefold() for entity in first.entities_involved}
        second_entities = {entity.casefold() for entity in second.entities_involved}
        shared_entities = sorted(first_entities & second_entities)
        return shared_tokens, shared_entities

    @staticmethod
    def _might_describe_same_event(
        first: TimelineEvent,
        second: TimelineEvent,
        shared_tokens: Sequence[str],
        shared_entities: Sequence[str],
    ) -> bool:
        """Use conservative signals to identify candidates for analyst review."""
        same_location = (
            bool(first.location)
            and first.location.casefold() == second.location.casefold()
        )
        same_category = first.category == second.category

        return (
            len(shared_tokens) >= 2
            or (bool(shared_entities) and (same_location or same_category))
            or (same_location and same_category and len(shared_tokens) >= 1)
        )

    def detect_correlations(
        self,
        time_window_minutes: float = 30.0,
    ) -> list[dict[str, Any]]:
        """Find potentially corroborating descriptions from distinct sources."""
        window = self._validate_nonnegative_finite(
            time_window_minutes,
            field_name="time_window_minutes",
        )
        events = self._sorted_events()
        correlations: list[dict[str, Any]] = []

        for index, first in enumerate(events):
            first_time = self._event_datetime(first)

            for second in events[index + 1 :]:
                time_difference = (
                    self._event_datetime(second) - first_time
                ).total_seconds() / 60

                if time_difference > window:
                    break
                if not first.source or not second.source:
                    continue
                if first.source.casefold() == second.source.casefold():
                    continue

                shared_tokens, shared_entities = self._semantic_overlap(first, second)
                if not self._might_describe_same_event(
                    first,
                    second,
                    shared_tokens,
                    shared_entities,
                ):
                    continue

                correlations.append(
                    {
                        "event_1": first.event_id,
                        "event_2": second.event_id,
                        "time_difference_minutes": round(time_difference, 2),
                        "source_1": first.source,
                        "source_2": second.source,
                        "shared_description_terms": shared_tokens,
                        "shared_entities": shared_entities,
                        "flag": "POTENTIAL_CORROBORATION",
                        "interpretation": (
                            "Potentially related accounts requiring analyst review; "
                            "this is not an automated identity determination."
                        ),
                    }
                )

        return correlations

    def detect_conflicts(
        self,
        *,
        minimum_difference_minutes: float = 30.0,
        candidate_window_hours: float = 24.0,
    ) -> list[dict[str, Any]]:
        """Find same-event candidates with materially different reported times.

        This flags discrepancies for review. It does not determine whether any
        source is inaccurate or whether two reports truly concern one event.
        """
        minimum_difference = self._validate_nonnegative_finite(
            minimum_difference_minutes,
            field_name="minimum_difference_minutes",
        )
        candidate_window = self._validate_nonnegative_finite(
            candidate_window_hours,
            field_name="candidate_window_hours",
        ) * 60

        if minimum_difference > candidate_window:
            raise ChronologyValidationError(
                "minimum_difference_minutes cannot exceed candidate_window_hours."
            )

        events = self._sorted_events()
        conflicts: list[dict[str, Any]] = []

        for index, first in enumerate(events):
            first_time = self._event_datetime(first)

            for second in events[index + 1 :]:
                difference_minutes = (
                    self._event_datetime(second) - first_time
                ).total_seconds() / 60

                if difference_minutes > candidate_window:
                    break
                if difference_minutes < minimum_difference:
                    continue
                if not first.source or not second.source:
                    continue
                if first.source.casefold() == second.source.casefold():
                    continue

                shared_tokens, shared_entities = self._semantic_overlap(first, second)
                if not self._might_describe_same_event(
                    first,
                    second,
                    shared_tokens,
                    shared_entities,
                ):
                    continue

                conflicts.append(
                    {
                        "event_1": first.event_id,
                        "event_2": second.event_id,
                        "time_difference_minutes": round(difference_minutes, 2),
                        "source_1": first.source,
                        "source_2": second.source,
                        "shared_description_terms": shared_tokens,
                        "shared_entities": shared_entities,
                        "flag": "TEMPORAL_DISCREPANCY",
                        "interpretation": (
                            "Potentially related reports have materially different "
                            "times. Verify timezone, clock accuracy, precision, and "
                            "whether they describe the same occurrence."
                        ),
                    }
                )

        return conflicts

    def entity_timeline(self, entity: str) -> list[TimelineEvent]:
        """Return events involving one named entity, case-insensitively."""
        normalized_entity = _normalize_text(entity, field_name="entity").casefold()
        if not normalized_entity:
            raise ChronologyValidationError("entity must not be empty.")

        return [
            event
            for event in self._sorted_events()
            if any(
                candidate.casefold() == normalized_entity
                for candidate in event.entities_involved
            )
        ]

    def category_breakdown(self) -> dict[str, int]:
        """Return deterministically ordered event counts by category."""
        counts = Counter(event.category for event in self.events)
        return dict(sorted(counts.items()))

    @staticmethod
    def _with_conflict_links(
        events: Sequence[TimelineEvent],
        conflicts: Sequence[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Build report-only conflict links without mutating timeline events."""
        linked_ids: dict[str, set[str]] = {
            event.event_id: set() for event in events
        }

        for conflict in conflicts:
            first = str(conflict["event_1"])
            second = str(conflict["event_2"])
            linked_ids[first].add(second)
            linked_ids[second].add(first)

        report_events: list[dict[str, Any]] = []
        for event in events:
            serialized = asdict(event)
            serialized["conflicts_with"] = sorted(linked_ids[event.event_id])
            report_events.append(serialized)

        return report_events

    def analyse(
        self,
        gap_threshold_hours: float = 24.0,
        correlation_window_minutes: float = 30.0,
        conflict_minimum_difference_minutes: float = 30.0,
        conflict_candidate_window_hours: float = 24.0,
    ) -> dict[str, Any]:
        """Return an idempotent full chronological analysis report."""
        sorted_events = self._sorted_events()
        gaps = self.detect_gaps(gap_threshold_hours)
        correlations = self.detect_correlations(correlation_window_minutes)
        conflicts = self.detect_conflicts(
            minimum_difference_minutes=conflict_minimum_difference_minutes,
            candidate_window_hours=conflict_candidate_window_hours,
        )

        entities = sorted(
            {
                entity
                for event in self.events
                for entity in event.entities_involved
            },
            key=str.casefold,
        )

        return {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "analysis_notes": [
                "All datetimes are normalized to UTC.",
                "Date-only and minute-precision values retain their source precision.",
                "Gaps identify absence of supplied timeline entries, not absence of activity.",
                "Correlations and discrepancies require analyst review.",
            ],
            "total_events": len(self.events),
            "date_range": {
                "earliest": sorted_events[0].utc_datetime if sorted_events else None,
                "latest": sorted_events[-1].utc_datetime if sorted_events else None,
            },
            "category_breakdown": self.category_breakdown(),
            "entities_mentioned": entities,
            "gaps": {
                "threshold_hours": gap_threshold_hours,
                "count": len(gaps),
                "items": gaps,
            },
            "correlations": {
                "window_minutes": correlation_window_minutes,
                "count": len(correlations),
                "items": correlations,
            },
            "temporal_discrepancies": {
                "minimum_difference_minutes": conflict_minimum_difference_minutes,
                "candidate_window_hours": conflict_candidate_window_hours,
                "count": len(conflicts),
                "items": conflicts,
            },
            "timeline": self._with_conflict_links(sorted_events, conflicts),
        }

    def export_csv(self, filepath: str | Path) -> Path:
        """Export the canonical event timeline as a UTF-8 spreadsheet-safe CSV."""
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "event_id",
            "utc_datetime",
            "original_datetime",
            "time_precision",
            "timezone_assumption",
            "category",
            "description",
            "source",
            "source_reliability",
            "info_credibility",
            "location",
            "entities_involved",
            "evidence_ref",
            "notes",
        ]

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()

            for event in self._sorted_events():
                row = asdict(event)
                row["entities_involved"] = "; ".join(event.entities_involved)
                writer.writerow(
                    {
                        name: _csv_safe(row.get(name, ""))
                        for name in fieldnames
                    }
                )

        try:
            temporary_path.replace(output_path)
        finally:
            temporary_path.unlink(missing_ok=True)

        return output_path


def _load_events(path: Path) -> list[dict[str, Any]]:
    """Load an event array or an object containing an event array."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ChronologyValidationError(f"Could not read input file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ChronologyValidationError(f"Invalid input JSON: {exc}") from exc

    events = document.get("events") if isinstance(document, dict) else document
    if not isinstance(events, list) or not events:
        raise ChronologyValidationError(
            "Input must be a non-empty JSON array or object with an 'events' array."
        )

    if not all(isinstance(event, dict) for event in events):
        raise ChronologyValidationError("Every event input row must be an object.")

    return events


def main() -> int:
    """Run timeline analysis from a JSON event document."""
    parser = argparse.ArgumentParser(description="Chronological matrix analyser")
    parser.add_argument("input", type=Path, help="JSON file with an events array")
    parser.add_argument(
        "--gap-hours",
        type=float,
        default=24.0,
        help="Minimum adjacent event gap to flag",
    )
    parser.add_argument(
        "--correlation-minutes",
        type=float,
        default=30.0,
        help="Maximum time difference for potential corroboration",
    )
    parser.add_argument(
        "--conflict-minutes",
        type=float,
        default=30.0,
        help="Minimum difference before a same-event candidate is discrepant",
    )
    parser.add_argument(
        "--conflict-window-hours",
        type=float,
        default=24.0,
        help="Maximum difference considered for temporal discrepancies",
    )
    parser.add_argument(
        "--naive-datetime-policy",
        choices=("reject", "utc", "assume_timezone"),
        default="reject",
        help="How to handle datetimes without an offset",
    )
    parser.add_argument(
        "--default-timezone",
        help="Fixed offset for --naive-datetime-policy assume_timezone, e.g. +01:00",
    )
    parser.add_argument("--output", "-o", type=Path, help="Output JSON report")
    parser.add_argument("--csv", type=Path, help="Output CSV timeline")
    args = parser.parse_args()

    try:
        input_events = _load_events(args.input)
        matrix = ChronologicalMatrix(
            naive_datetime_policy=args.naive_datetime_policy,
            default_timezone=args.default_timezone,
        )

        row_errors: list[str] = []
        for index, event in enumerate(input_events, start=1):
            try:
                matrix.add_event(
                    datetime_str=event.get("datetime", event.get("timestamp", "")),
                    description=event.get("description", ""),
                    source=event.get("source", ""),
                    source_reliability=event.get("source_reliability", ""),
                    info_credibility=event.get("info_credibility", ""),
                    entities=event.get("entities"),
                    location=event.get("location", ""),
                    category=event.get("category", DEFAULT_CATEGORY),
                    evidence_ref=event.get("evidence_ref", ""),
                    notes=event.get("notes", ""),
                )
            except (ChronologyValidationError, TypeError) as exc:
                row_errors.append(f"row {index}: {exc}")

        if row_errors:
            print("Chronology validation failed:", file=sys.stderr)
            for error in row_errors:
                print(f"  - {error}", file=sys.stderr)
            print("No chronology outputs were written.", file=sys.stderr)
            return 2

        report = matrix.analyse(
            gap_threshold_hours=args.gap_hours,
            correlation_window_minutes=args.correlation_minutes,
            conflict_minimum_difference_minutes=args.conflict_minutes,
            conflict_candidate_window_hours=args.conflict_window_hours,
        )
    except ChronologyValidationError as exc:
        print(f"Chronology analysis failed: {exc}", file=sys.stderr)
        return 2

    print(
        "Timeline: "
        f"{report['total_events']} events, "
        f"{report['gaps']['count']} gaps, "
        f"{report['correlations']['count']} correlations, "
        f"{report['temporal_discrepancies']['count']} temporal discrepancies"
    )

    if args.output is not None:
        _atomic_write_text(args.output, json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"JSON report exported to {args.output}")

    if args.csv is not None:
        matrix.export_csv(args.csv)
        print(f"CSV timeline exported to {args.csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
