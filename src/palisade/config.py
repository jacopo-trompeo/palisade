import logging
from dataclasses import dataclass
from pathlib import Path

HOSTS_MARKER_START = "# === PALISADE START ==="
HOSTS_MARKER_END = "# === PALISADE END ==="


@dataclass(frozen=True)
class _Paths:
    db: Path
    hosts: Path
    socket: Path


_DEV_PATHS = _Paths(
    db=Path("/tmp/palisade_dev.db"),
    hosts=Path("/tmp/palisade_hosts_preview"),
    socket=Path("/tmp/palisade_dev.sock"),
)
_PROD_PATHS = _Paths(
    db=Path("/var/lib/palisade/palisade.db"),
    hosts=Path("/etc/hosts"),
    socket=Path("/run/palisade/palisade.sock"),
)

_dev = False
_paths = _PROD_PATHS


def configure(dev: bool) -> None:
    global _dev, _paths
    _dev = dev
    _paths = _DEV_PATHS if dev else _PROD_PATHS


def setup_logging(dev: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if dev else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def is_dev() -> bool:
    return _dev


def db_path() -> Path:
    return _paths.db


def hosts_path() -> Path:
    return _paths.hosts


def socket_path() -> Path:
    return _paths.socket
