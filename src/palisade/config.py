import sys
from pathlib import Path

DEV_MODE: bool = "--dev" in sys.argv

if DEV_MODE:
    DB_PATH = Path("/tmp/palisade_dev.db")
    HOSTS_PATH = Path("/tmp/palisade_hosts_preview")
else:
    DB_PATH = Path("/var/lib/palisade/palisade.db")
    HOSTS_PATH = Path("/etc/hosts")

HOSTS_MARKER_START = "# === PALISADE START ==="
HOSTS_MARKER_END = "# === PALISADE END ==="


def log_dev(component: str, action: str) -> None:
    if DEV_MODE:
        print(f"[PALISADE DEV] {component}: {action}", flush=True)
