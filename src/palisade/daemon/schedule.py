from datetime import datetime, time, timedelta

from palisade.db.models import Filter, Schedule, ScheduleType, TimeRange


def _hhmm_to_time(s: str) -> time:
    h, m = s.split(":")

    return time(int(h), int(m))


def _in_range(now_t: time, tr: TimeRange) -> bool:
    start = _hhmm_to_time(tr.start)
    end = _hhmm_to_time(tr.end)

    if start <= end:
        return start <= now_t <= end

    return now_t >= start or now_t <= end


def is_active(f: Filter, now: datetime) -> bool:
    if not f.enabled:
        return False

    s = f.schedule

    if s.type == ScheduleType.ALWAYS:
        return True

    if now.weekday() not in s.days:
        return False
    now_t = now.time().replace(second=0, microsecond=0)

    return any(_in_range(now_t, tr) for tr in s.time_ranges)


def _candidate_transitions_for_day(s: Schedule, day_start: datetime) -> list[datetime]:
    if s.type == ScheduleType.ALWAYS:
        return []

    result: list[datetime] = []

    for tr in s.time_ranges:
        start_t = _hhmm_to_time(tr.start)
        end_t = _hhmm_to_time(tr.end)
        start_dt = day_start.replace(hour=start_t.hour, minute=start_t.minute)
        result.append(start_dt)

        if start_t <= end_t:
            end_dt = day_start.replace(hour=end_t.hour, minute=end_t.minute)
            result.append(end_dt + timedelta(minutes=1))
        else:
            end_dt = day_start + timedelta(
                days=1, hours=end_t.hour, minutes=end_t.minute
            )
            result.append(end_dt + timedelta(minutes=1))

    return result


def next_transition(filters: list[Filter], now: datetime) -> datetime:
    candidates: list[datetime] = []

    for f in filters:
        if not f.enabled or f.schedule.type == ScheduleType.ALWAYS:
            continue

        for delta in range(8):
            day = (now + timedelta(days=delta)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            weekday = day.weekday()
            if weekday in f.schedule.days:
                candidates.extend(_candidate_transitions_for_day(f.schedule, day))

            yday = day - timedelta(days=1)
            if yday.weekday() in f.schedule.days:
                for tr in f.schedule.time_ranges:
                    if _hhmm_to_time(tr.start) > _hhmm_to_time(tr.end):
                        end_t = _hhmm_to_time(tr.end)
                        spill_end = day.replace(hour=end_t.hour, minute=end_t.minute)
                        candidates.append(spill_end + timedelta(minutes=1))

    future = [c for c in candidates if c > now]

    if not future:
        return now + timedelta(days=7)

    return min(future)
