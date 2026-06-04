import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication

from palisade.dbi import get_setting

logger = logging.getLogger(__name__)

THEMES_DIR = Path(__file__).parent.parent / "assets" / "themes"


def current_theme() -> str:
    try:
        val = (get_setting("theme") or "dark").strip().lower()
    except Exception as exc:
        logger.warning("could not read theme setting, defaulting to dark: %s", exc)
        val = "dark"
    return "light" if val == "light" else "dark"


def apply_theme(theme_name: str | None = None) -> None:
    if theme_name is None:
        theme_name = current_theme()

    theme_file = THEMES_DIR / f"{theme_name}.qss"

    app = QApplication.instance()
    if not isinstance(app, QApplication):
        return

    if not theme_file.exists():
        return

    app.setStyleSheet(theme_file.read_text())
