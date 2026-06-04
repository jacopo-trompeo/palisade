import asyncio
import contextlib
import logging
from datetime import datetime

import psutil

from palisade import config
from palisade.daemon.enforcer import (
    EnforcementSnapshot,
    build_snapshot,
    enforce_processes,
    notify_user,
    write_hosts,
)
from palisade.daemon.schedule import is_active, next_transition
from palisade.db import database as _db
from palisade.db.database import init_db, list_filters
from palisade.db.models import Filter
from palisade.ipc import serve

logger = logging.getLogger(__name__)

_snapshot: EnforcementSnapshot = EnforcementSnapshot(set(), set(), {}, {})
_already_notified_pids: set[int] = set()
_changed_event: asyncio.Event | None = None


def _recompute_snapshot(now: datetime) -> EnforcementSnapshot:
    filters = list_filters()
    active = [f for f in filters if is_active(f, now)]
    snap = build_snapshot(active)

    logger.debug(
        "recompute @ %s: %d/%d active, %d domains, %d apps",
        now.isoformat(timespec="seconds"),
        len(active),
        len(filters),
        len(snap.domains),
        len(snap.apps),
    )

    return snap


def _apply_snapshot(snap: EnforcementSnapshot) -> None:
    global _snapshot
    _snapshot = snap
    write_hosts(snap.domains)


async def _schedule_loop() -> None:
    global _changed_event
    _changed_event = asyncio.Event()

    while True:
        now = datetime.now()
        snap = _recompute_snapshot(now)
        _apply_snapshot(snap)

        nt = next_transition(list_filters(), now)
        wait_s = max(1.0, (nt - now).total_seconds())
        logger.debug(
            "next transition at %s (in %ds)",
            nt.isoformat(timespec="seconds"),
            int(wait_s),
        )
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(_changed_event.wait(), timeout=wait_s)
        _changed_event.clear()


async def _process_monitor_loop() -> None:
    global _already_notified_pids

    while True:
        snap = _snapshot
        if snap.apps:
            matches = await enforce_processes(snap.apps, snap.filter_name_by_app)
            for pid, name, app in matches:
                if pid in _already_notified_pids:
                    continue
                _already_notified_pids.add(pid)
                filter_name = snap.filter_name_by_app.get(app, "Palisade")
                notify_user(
                    "Palisade - app blocked",
                    f"{name} was closed because filter '{filter_name}' is active.",
                )
        live_pids = {p.pid for p in psutil.process_iter(["pid"])}
        _already_notified_pids &= live_pids

        await asyncio.sleep(config.PROCESS_POLL_INTERVAL_SEC)


def _mark_dirty() -> None:
    if _changed_event is not None:
        _changed_event.set()


async def _handle_ipc(msg: dict) -> dict | None:
    t = msg.get("type")

    if t == "ping":
        return {"type": "pong"}
    if t == "filters_changed":
        _mark_dirty()
        return {"type": "ack"}
    if t == "get_status":
        return {
            "type": "status",
            "domains": sorted(_snapshot.domains),
            "apps": sorted(_snapshot.apps),
        }

    try:
        if t == "db.list_filters":
            return {
                "type": "ok",
                "filters": [f.to_dict() for f in _db.list_filters()],
            }
        if t == "db.get_filter":
            f = _db.get_filter(msg["id"])
            return {"type": "ok", "filter": f.to_dict() if f else None}
        if t == "db.create_filter":
            _db.create_filter(Filter.from_dict(msg["filter"]))
            _mark_dirty()
            return {"type": "ok"}
        if t == "db.update_filter":
            _db.update_filter(Filter.from_dict(msg["filter"]))
            _mark_dirty()
            return {"type": "ok"}
        if t == "db.delete_filter":
            _db.delete_filter(msg["id"])
            _mark_dirty()
            return {"type": "ok"}
        if t == "db.get_setting":
            return {"type": "ok", "value": _db.get_setting(msg["key"])}
        if t == "db.set_setting":
            _db.set_setting(msg["key"], msg["value"])
            return {"type": "ok"}
        if t == "db.get_edit_lock_seconds":
            return {"type": "ok", "value": _db.get_edit_lock_seconds()}
        if t == "db.set_edit_lock_seconds":
            _db.set_edit_lock_seconds(int(msg["value"]))
            return {"type": "ok"}
    except (KeyError, TypeError, ValueError) as e:
        return {"type": "error", "message": f"bad request: {e}"}

    return {"type": "error", "message": f"unknown message type: {t}"}


async def _amain() -> int:
    config.db_path().parent.mkdir(parents=True, exist_ok=True)
    config.socket_path().parent.mkdir(parents=True, exist_ok=True)

    init_db()
    server = await serve(_handle_ipc)
    logger.info("daemon started, IPC server listening on %s", config.socket_path())
    schedule_task = asyncio.create_task(_schedule_loop())
    monitor_task = asyncio.create_task(_process_monitor_loop())

    try:
        async with server:
            await asyncio.gather(schedule_task, monitor_task)
    finally:
        with contextlib.suppress(Exception):
            write_hosts(set())
    return 0


def run() -> int:
    try:
        return asyncio.run(_amain())
    except KeyboardInterrupt:
        return 0
