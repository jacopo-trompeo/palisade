from pathlib import Path

from PySide6.QtWidgets import QApplication

THEMES_DIR = Path(__file__).parent.parent / "assets" / "themes"


def apply_theme(theme_name: str = "dark") -> None:
    theme_file = THEMES_DIR / f"{theme_name}.qss"

    app = QApplication.instance()
    if not isinstance(app, QApplication):
        return

    if not theme_file.exists():
        return

    app.setStyleSheet(theme_file.read_text())
