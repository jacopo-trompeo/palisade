from palisade.db import database
from palisade.db.models import Filter, Schedule, ScheduleType, TimeRange


def _make_filter() -> Filter:
    return Filter(
        name="Focus",
        schedule=Schedule(
            type=ScheduleType.CUSTOM,
            days=[0, 1, 2, 3, 4],
            time_ranges=[TimeRange("09:00", "17:00")],
        ),
        blocked_websites=["reddit.com"],
        blocked_apps=["discord"],
        enabled=True,
    )


def test_create_get_round_trip(temp_db):
    f = _make_filter()
    database.create_filter(f)
    got = database.get_filter(f.id)
    assert got == f


def test_list_and_delete(temp_db):
    f = _make_filter()
    database.create_filter(f)
    assert [x.id for x in database.list_filters()] == [f.id]
    database.delete_filter(f.id)
    assert database.list_filters() == []


def test_update(temp_db):
    f = _make_filter()
    database.create_filter(f)
    f.name = "Renamed"
    f.enabled = False
    database.update_filter(f)
    got = database.get_filter(f.id)
    assert got is not None
    assert got.name == "Renamed"
    assert got.enabled is False


def test_settings_upsert(temp_db):
    assert database.get_setting("theme") is None
    assert database.get_setting("theme", "dark") == "dark"
    database.set_setting("theme", "light")
    assert database.get_setting("theme") == "light"
    database.set_setting("theme", "dark")
    assert database.get_setting("theme") == "dark"
