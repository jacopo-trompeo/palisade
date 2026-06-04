import pytest

from palisade.db.models import (
    Filter,
    Schedule,
    ScheduleType,
    TimeRange,
    is_valid_domain,
)


def test_time_range_valid():
    tr = TimeRange("09:00", "17:00")
    assert tr.to_dict() == {"start": "09:00", "end": "17:00"}
    assert TimeRange.from_dict(tr.to_dict()) == tr


@pytest.mark.parametrize(
    "start,end", [("9:00", "17:00"), ("09:60", "10:00"), ("24:00", "25:00")]
)
def test_time_range_invalid_format(start, end):
    with pytest.raises(ValueError):
        TimeRange(start, end)


def test_time_range_overnight_rejected():
    with pytest.raises(ValueError):
        TimeRange("17:00", "09:00")


def test_schedule_type_coerced_from_str():
    assert Schedule(type="custom").type is ScheduleType.CUSTOM  # type: ignore[arg-type]
    assert Schedule(type="always").type is ScheduleType.ALWAYS  # type: ignore[arg-type]


def test_schedule_json_round_trip():
    s = Schedule(
        type=ScheduleType.CUSTOM,
        days=[0, 1, 4],
        time_ranges=[TimeRange("08:00", "12:00")],
    )
    assert Schedule.from_json(s.to_json()) == s


def test_schedule_from_dict_defaults_match_constructor():
    s = Schedule.from_dict({"type": "always"})
    assert s.days == list(range(7))
    assert s.time_ranges == [TimeRange("00:00", "23:59")]


def test_schedule_summary():
    assert Schedule(type=ScheduleType.ALWAYS).summary() == "Always"
    weekdays = Schedule(type=ScheduleType.CUSTOM, days=[0, 1, 2, 3, 4])
    assert weekdays.summary().startswith("Weekdays")


@pytest.mark.parametrize("domain", ["youtube.com", "sub.example.co.uk"])
def test_valid_domains(domain):
    assert is_valid_domain(domain)


@pytest.mark.parametrize("bad", ["", "http://x.com", "no spaces .com", "nodot"])
def test_invalid_domains(bad):
    assert not is_valid_domain(bad)


def test_filter_normalizes_and_dedupes_websites():
    f = Filter(blocked_websites=["A.COM", "a.com", "b.com"])
    assert f.blocked_websites == ["a.com", "b.com"]


def test_filter_rejects_invalid_domain():
    with pytest.raises(ValueError):
        Filter(blocked_websites=["not a domain"])


def test_filter_sets_created_at():
    assert Filter().created_at


def test_filter_dict_round_trip():
    f = Filter(
        name="Focus",
        schedule=Schedule(type=ScheduleType.CUSTOM, days=[5, 6]),
        blocked_websites=["reddit.com"],
        blocked_apps=["steam", "steam"],
        enabled=False,
    )
    assert Filter.from_dict(f.to_dict()) == f


def test_filter_row_round_trip():
    f = Filter(name="X", blocked_apps=["discord"])
    assert Filter.from_row(f.to_row()) == f


def test_filter_summary_pluralization():
    f = Filter(blocked_websites=["a.com"], blocked_apps=["x", "y"])
    assert f.summary() == "1 site · 2 apps"
