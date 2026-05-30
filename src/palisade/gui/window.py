from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from palisade.config import DEV_MODE
from palisade.gui.theme import apply_theme
from palisade.gui.widgets.dev_banner import DevBanner
from palisade.gui.widgets.sidebar import Sidebar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palisade")
        self.resize(960, 640)

        apply_theme()

        self._build_layout()
        self._build_pages()

    def _build_layout(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        if DEV_MODE:
            root_layout.addWidget(DevBanner())

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        root_layout.addWidget(body, 1)

        self._sidebar = Sidebar()
        self._sidebar.nav_requested.connect(self._on_nav)
        body_layout.addWidget(self._sidebar)

        self._pages = QStackedWidget()
        self._pages.setObjectName("PageArea")
        body_layout.addWidget(self._pages, 1)

    def _build_pages(self) -> None:
        from palisade.gui.views.about import AboutPage
        from palisade.gui.views.home import HomePage
        from palisade.gui.views.settings import SettingsPage

        self._home = HomePage()
        self._settings = SettingsPage()
        self._about = AboutPage()

        self._page_keys: dict[str, int] = {}

        for key, w in (
            ("home", self._home),
            ("settings", self._settings),
            ("about", self._about),
        ):
            self._page_keys[key] = self._pages.addWidget(w)

    def _on_nav(self, key: str) -> None:
        if key not in self._page_keys:
            return
        self._pages.setCurrentIndex(self._page_keys[key])
