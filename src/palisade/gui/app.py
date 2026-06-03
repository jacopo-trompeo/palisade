import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from palisade import config


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

    icon = QIcon.fromTheme("system-lock-screen")
    if icon.isNull():
        icon = QIcon.fromTheme("application-x-executable")
    app.setWindowIcon(icon)

    from palisade.gui.window import Window

    win = Window()
    win.show()

    return app.exec()
