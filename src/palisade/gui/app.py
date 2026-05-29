from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


def run() -> int:
    app = QApplication.instance()
    if not isinstance(app, QApplication):
        app = QApplication(sys.argv)

    app.setApplicationName("Palisade")
    app.setApplicationDisplayName("Palisade")

    icon = QIcon.fromTheme("system-lock-screen")
    if icon.isNull():
        icon = QIcon.fromTheme("application-x-executable")
    app.setWindowIcon(icon)

    from palisade.gui.window import Window

    win = Window()
    win.show()

    return app.exec()
