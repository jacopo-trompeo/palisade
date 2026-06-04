import logging
import os
import socket as _socket
import subprocess
import sys
import textwrap
import time
from pathlib import Path

from palisade import config

logger = logging.getLogger(__name__)

DAEMON_DIRS = [Path("/var/lib/palisade"), Path("/run/palisade")]
DAEMON_READY_TIMEOUT_SEC = 30


def generate_unit_file(python_exe: str) -> str:
    return textwrap.dedent(
        f"""\
        [Unit]
        Description=Palisade productivity filter daemon
        After=network.target

        [Service]
        Type=simple
        ExecStart={python_exe} -m palisade --daemon
        Restart=on-failure
        RestartSec=5
        User=root

        [Install]
        WantedBy=multi-user.target
        """
    )


def _run(cmd: list[str]) -> None:
    logger.info("$ %s", " ".join(cmd))
    subprocess.run(cmd, check=True)


def _ensure_root() -> None:
    if os.geteuid() != 0:
        sys.stderr.write(
            "Palisade installer must run as root. Invoke this via pkexec from the "
            "GUI, or `sudo python -m palisade --install-daemon` from a terminal.\n"
        )
        sys.exit(1)


def _ping_daemon_once() -> bool:
    try:
        s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(str(config.socket_path()))
        try:
            s.sendall(b'{"type":"ping"}\n')
            data = s.recv(4096)
        finally:
            s.close()
        return b'"pong"' in data
    except (FileNotFoundError, ConnectionRefusedError, OSError, TimeoutError):
        return False


def _wait_for_daemon(timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _ping_daemon_once():
            return True
        time.sleep(0.3)
    return False


def _dump_diagnostics() -> None:
    sys.stderr.write("\n[palisade-install] DIAGNOSTICS:\n\n")
    sys.stderr.flush()
    subprocess.run(
        ["systemctl", "status", "--no-pager", config.SYSTEMD_UNIT_NAME],
        stdout=sys.stderr,
        stderr=sys.stderr,
        check=False,
    )
    sys.stderr.write("\n[palisade-install] Recent journal lines:\n\n")
    sys.stderr.flush()
    subprocess.run(
        [
            "journalctl",
            "-u",
            config.SYSTEMD_UNIT_NAME,
            "-n",
            "30",
            "--no-pager",
        ],
        stdout=sys.stderr,
        stderr=sys.stderr,
        check=False,
    )


def install() -> int:
    _ensure_root()

    python_exe = sys.executable
    unit_text = generate_unit_file(python_exe)
    unit_path = config.UNIT_FILE_PATH
    logger.info("writing %s", unit_path)
    unit_path.parent.mkdir(parents=True, exist_ok=True)
    unit_path.write_text(unit_text)
    unit_path.chmod(0o644)

    for d in DAEMON_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    _run(["systemctl", "daemon-reload"])
    _run(["systemctl", "enable", "--now", config.SYSTEMD_UNIT_NAME])

    logger.info(
        "waiting up to %ds for daemon to respond on %s...",
        DAEMON_READY_TIMEOUT_SEC,
        config.socket_path(),
    )
    if not _wait_for_daemon(DAEMON_READY_TIMEOUT_SEC):
        sys.stderr.write(
            f"\n[palisade-install] ERROR: daemon installed but did not start "
            f"responding within {DAEMON_READY_TIMEOUT_SEC}s.\n"
        )
        sys.stderr.flush()
        _dump_diagnostics()
        return 2

    logger.info("done - daemon is running and responsive.")
    return 0


def uninstall() -> int:
    _ensure_root()

    subprocess.run(["systemctl", "disable", "--now", config.SYSTEMD_UNIT_NAME])

    unit_path = config.UNIT_FILE_PATH
    if unit_path.exists():
        logger.info("removing %s", unit_path)
        unit_path.unlink()
        _run(["systemctl", "daemon-reload"])

    logger.info("uninstalled.")
    return 0
