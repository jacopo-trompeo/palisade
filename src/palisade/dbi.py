from palisade.config import is_dev
from palisade.db.database import (
    EDIT_LOCK_SECONDS_MAX as EDIT_LOCK_SECONDS_MAX,
)
from palisade.db.database import (
    EDIT_LOCK_SECONDS_MIN as EDIT_LOCK_SECONDS_MIN,
)
from palisade.db.models import Filter


class DaemonUnavailable(RuntimeError):
    pass


def _rpc(msg: dict) -> dict:
    from palisade import ipc

    reply = ipc.notify(msg, timeout=3.0)
    if reply is None:
        raise DaemonUnavailable(
            "Palisade daemon not reachable. "
            "Install or start it via the system settings."
        )
    if reply.get("type") == "error":
        raise RuntimeError(reply.get("message", "daemon error"))
    return reply


def list_filters() -> list[Filter]:
    if is_dev():
        from palisade.db.database import list_filters as _list_filters

        return _list_filters()
    else:
        reply = _rpc({"type": "db.list_filters"})
        return [Filter.from_dict(d) for d in reply["filters"]]


def get_filter(filter_id: str) -> Filter | None:
    if is_dev():
        from palisade.db.database import get_filter as _get_filter

        return _get_filter(filter_id)
    else:
        reply = _rpc({"type": "db.get_filter", "id": filter_id})
        d = reply.get("filter")
        return Filter.from_dict(d) if d else None


def create_filter(f: Filter) -> None:
    if is_dev():
        from palisade.db.database import create_filter as _create_filter

        _create_filter(f)
    else:
        _rpc({"type": "db.create_filter", "filter": f.to_dict()})


def update_filter(f: Filter) -> None:
    if is_dev():
        from palisade.db.database import update_filter as _update_filter

        _update_filter(f)
    else:
        _rpc({"type": "db.update_filter", "filter": f.to_dict()})


def delete_filter(filter_id: str) -> None:
    if is_dev():
        from palisade.db.database import delete_filter as _delete_filter

        _delete_filter(filter_id)
    else:
        _rpc({"type": "db.delete_filter", "id": filter_id})


def get_setting(key: str, default: str | None = None) -> str | None:
    if is_dev():
        from palisade.db.database import get_setting as _get_setting

        return _get_setting(key, default)
    else:
        reply = _rpc({"type": "db.get_setting", "key": key})
        value = reply.get("value")
        return value if value is not None else default


def set_setting(key: str, value: str) -> None:
    if is_dev():
        from palisade.db.database import set_setting as _set_setting

        _set_setting(key, value)
    else:
        _rpc({"type": "db.set_setting", "key": key, "value": value})


def get_edit_lock_seconds() -> int:
    if is_dev():
        from palisade.db.database import (
            get_edit_lock_seconds as _get_edit_lock_seconds,
        )

        return _get_edit_lock_seconds()
    else:
        reply = _rpc({"type": "db.get_edit_lock_seconds"})
        return int(reply["value"])


def set_edit_lock_seconds(seconds: int) -> None:
    if is_dev():
        from palisade.db.database import (
            set_edit_lock_seconds as _set_edit_lock_seconds,
        )

        _set_edit_lock_seconds(seconds)
    else:
        _rpc({"type": "db.set_edit_lock_seconds", "value": int(seconds)})
