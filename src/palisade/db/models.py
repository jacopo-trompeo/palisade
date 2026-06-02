import json
import re
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

ScheduleType = Literal["always", "custom"]

_DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$",
    re.IGNORECASE,
)

_TIME_REGEX = re.compile(r"^([01][0-9]|2[0-3]):([0-5][0-9])$")


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_domain(s: str) -> str:
    s = s.strip().lower()
    if s.endswith("."):
        s = s[:-1]
    return s


def is_valid_domain(s: str) -> bool:
    if not s or s != s.strip():
        return False
    return _DOMAIN_REGEX.match(s) is not None


@dataclass
class TimeRange:
    start: str
    end: str

    def __post_init__(self) -> None:
        if not _TIME_REGEX.match(self.start):
            raise ValueError(f"invalid start time: {self.start!r} (expected HH:MM)")
        if not _TIME_REGEX.match(self.end):
            raise ValueError(f"invalid end time: {self.end!r} (expected HH:MM)")

        if self.start >= self.end:
            raise ValueError(
                f"time range start must be before end "
                f"({self.start} >= {self.end}); overnight ranges are unsupported"
            )

    def to_dict(self) -> dict:
        return {"start": self.start, "end": self.end}

    @classmethod
    def from_dict(cls, d: dict) -> TimeRange:
        return cls(start=d["start"], end=d["end"])


@dataclass
class Schedule:
    type: ScheduleType = "always"
    days: list[int] = field(default_factory=lambda: list(range(7)))
    time_ranges: list[TimeRange] = field(
        default_factory=lambda: [TimeRange("00:00", "23:59")]
    )

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "days": list(self.days),
            "time_ranges": [tr.to_dict() for tr in self.time_ranges],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict) -> Schedule:
        return cls(
            type=d.get("type", "always"),
            days=d.get("days", list(range(7))),
            time_ranges=[TimeRange.from_dict(tr) for tr in d.get("time_ranges", [])],
        )

    @classmethod
    def from_json(cls, s: str) -> Schedule:
        return cls.from_dict(json.loads(s))

    def summary(self) -> str:
        if self.type == "always":
            return "Always"

        day_set = set(self.days)
        if day_set == set(range(7)):
            days_str = "Every day"
        elif day_set == {0, 1, 2, 3, 4}:
            days_str = "Weekdays"
        elif day_set == {5, 6}:
            days_str = "Weekends"
        else:
            names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
            days_str = " ".join(names[d] for d in sorted(self.days))

        if not self.time_ranges:
            return days_str
        ranges_str = ", ".join(f"{tr.start}–{tr.end}" for tr in self.time_ranges)
        return f"{days_str}, {ranges_str}"


@dataclass
class Filter:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    schedule: Schedule = field(default_factory=Schedule)
    blocked_websites: list[str] = field(default_factory=list)
    blocked_apps: list[str] = field(default_factory=list)
    enabled: bool = True
    created_at: str = ""

    def __post_init__(self) -> None:
        now = _utcnow_iso()
        if not self.created_at:
            self.created_at = now

        self.blocked_websites = list(
            dict.fromkeys(_normalize_domain(w) for w in self.blocked_websites)
        )
        for w in self.blocked_websites:
            if not is_valid_domain(w):
                raise ValueError(f"invalid domain in blocked_websites: {w!r}")

        self.blocked_apps = list(dict.fromkeys(self.blocked_apps))

    def to_row(self) -> tuple:
        now = datetime.now(timezone.utc).isoformat()
        created = self.created_at or now
        return (
            self.id,
            self.name,
            self.schedule.to_json(),
            json.dumps(self.blocked_websites),
            json.dumps(self.blocked_apps),
            1 if self.enabled else 0,
            created,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "schedule": self.schedule.to_dict(),
            "blocked_websites": list(self.blocked_websites),
            "blocked_apps": list(self.blocked_apps),
            "enabled": self.enabled,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Filter:
        return cls(
            id=d["id"],
            name=d.get("name", ""),
            schedule=Schedule.from_dict(d.get("schedule", {})),
            blocked_websites=list(d.get("blocked_websites", [])),
            blocked_apps=list(d.get("blocked_apps", [])),
            enabled=bool(d.get("enabled", True)),
            created_at=d.get("created_at", ""),
        )

    @classmethod
    def from_row(cls, row: tuple | Mapping) -> Filter:
        if hasattr(row, "keys"):
            r = dict(row)
        else:
            row_columns = (
                "id",
                "name",
                "schedule_json",
                "blocked_websites_json",
                "blocked_apps_json",
                "enabled",
                "created_at",
            )
            r = dict(zip(row_columns, row))
        return cls(
            id=r["id"],
            name=r["name"],
            schedule=Schedule.from_json(r["schedule_json"]),
            blocked_websites=json.loads(r["blocked_websites_json"]),
            blocked_apps=json.loads(r["blocked_apps_json"]),
            enabled=bool(r["enabled"]),
            created_at=r["created_at"],
        )

    def summary(self) -> str:
        return (
            f"{len(self.blocked_websites)} site"
            f"{'s' if len(self.blocked_websites) != 1 else ''} · "
            f"{len(self.blocked_apps)} app"
            f"{'s' if len(self.blocked_apps) != 1 else ''}"
        )
