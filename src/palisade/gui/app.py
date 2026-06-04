import logging
import os
import subprocess
import sys
import time

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from palisade import config

logger = logging.getLogger(__name__)


def _poll_ping(seconds: float = 10.0) -> bool:
    from palisade import ipc

    deadline = seconds * 5
    for _ in range(int(deadline)):
        if ipc.ping():
            return True
        QApplication.processEvents()
        time.sleep(0.2)
    return False


def _spawn_dev_daemon() -> None:
    env = os.environ.copy()
    subprocess.Popen(
        [sys.executable, "-m", "palisade", "--dev", "--daemon"],
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,
        start_new_session=True,
    )
    _poll_ping(seconds=2.0)


def _ask(title: str, text: str) -> bool:
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Question)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    box.setDefaultButton(QMessageBox.StandardButton.Yes)

    return box.exec() == QMessageBox.StandardButton.Yes


def _warn_daemon_down(detail: str, diagnostics: str = "") -> None:
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle("Palisade daemon not running")
    box.setText("Palisade is not enforcing any blocks right now.")
    box.setInformativeText(detail)

    if diagnostics.strip():
        box.setDetailedText(diagnostics)

    box.exec()


def _run_privileged(cmd: list[str]) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout or "") + (result.stderr or "")

    return result.returncode, output


def _ensure_prod_daemon() -> None:
    if config.UNIT_FILE_PATH.exists():
        if not _ask(
            "Start Palisade daemon?",
            "Palisade's background service is installed but not running. "
            "Start it now?\n"
            "You'll be prompted for your administrator password.",
        ):
            _warn_daemon_down(
                "You declined to start the daemon. Restart Palisade to retry."
            )
            return
        rc, output = _run_privileged(
            ["pkexec", "systemctl", "start", config.SYSTEMD_UNIT_NAME]
        )
    else:
        if not _ask(
            "Install Palisade daemon?",
            "Palisade needs a small background service to enforce blocks "
            "even when this window is closed. Install it now?\n"
            "You'll be prompted for your administrator password.\n\n"
            "Note: this can take up to 30 seconds while the daemon starts up.",
        ):
            _warn_daemon_down(
                "You declined to install the daemon. Restart Palisade to retry."
            )
            return
        rc, output = _run_privileged(
            ["pkexec", sys.executable, "-m", "palisade", "--install-daemon"]
        )

    if rc != 0:
        _warn_daemon_down(
            f"The privileged step exited with code {rc}.\n"
            "Click 'Show Details' for the captured output.",
            diagnostics=output,
        )
        return

    if not _poll_ping(seconds=15.0):
        _warn_daemon_down(
            "The privileged step finished, but the daemon isn't responding. "
            "Check `systemctl status palisade-daemon` and "
            "`journalctl -u palisade-daemon -n 50`.",
            diagnostics=output,
        )


def _ensure_daemon() -> bool:
    from palisade import ipc

    if ipc.ping():
        return True
    if config.is_dev():
        _spawn_dev_daemon()
    else:
        _ensure_prod_daemon()

    return ipc.ping()


def run(dev: bool = False) -> int:
    config.configure(dev)
    config.setup_logging(dev)

    if dev:
        from palisade.db.database import init_db

        init_db()

    app = QApplication.instance()
    if not isinstance(app, QApplication):
        app = QApplication(sys.argv)

    app.setApplicationName("Palisade")
    app.setApplicationDisplayName("Palisade")
    app.setQuitOnLastWindowClosed(False)

    icon = QIcon.fromTheme("system-lock-screen")
    if icon.isNull():
        icon = QIcon.fromTheme("application-x-executable")
    app.setWindowIcon(icon)

    if not _ensure_daemon():
        return 1

    from palisade.gui.window import Window

    win = Window()
    win.show()

    return app.exec()
