from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from palisade.config import DEV_MODE
from palisade.gui.theme import apply_theme
from palisade.gui.views.filter_editor import FilterEditorView
from palisade.gui.widgets.dev_banner import DevBanner
from palisade.gui.widgets.sidebar import Sidebar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Palisade")
        self.resize(960, 640)

        apply_theme()

        self._build_layout()
        self._build_views()

        self.navigate("home")

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
        self._sidebar.nav_requested.connect(self.navigate)
        body_layout.addWidget(self._sidebar)

        self._views = QStackedWidget()
        self._views.setObjectName("ViewArea")
        body_layout.addWidget(self._views, 1)

    def _build_views(self) -> None:
        from palisade.gui.views.about import AboutView
        from palisade.gui.views.home import HomeView
        from palisade.gui.views.settings import SettingsView

        self._home = HomeView()
        self._settings = SettingsView()
        self._about = AboutView()
        self._filter_editor = FilterEditorView(self)

        self._view_keys: dict[str, int] = {
            "home": self._views.addWidget(self._home),
            "settings": self._views.addWidget(self._settings),
            "about": self._views.addWidget(self._about),
            "filter_editor": self._views.addWidget(self._filter_editor),
        }

        self._home.filter_nav_requested.connect(lambda: self.navigate("filter_editor"))

    def navigate(self, key: str) -> None:
        if key not in self._view_keys:
            return
        self._sidebar.set_active_index(key)
        self._views.setCurrentIndex(self._view_keys[key])
