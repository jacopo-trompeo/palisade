import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

SIDEBAR_ITEMS = [
    ("home", "Home", "fa6s.house"),
    ("settings", "Settings", "fa6s.gear"),
    ("about", "About", "fa6s.circle-info"),
]

_ICON_SIZE = QSize(18, 18)


class _SidebarButton(QPushButton):
    def __init__(self, label: str, icon_name: str):
        super().__init__(f"  {label}")

        self.setObjectName("SidebarButton")
        self.setIcon(qta.icon(icon_name, color="#b4b4bd"))
        self.setIconSize(_ICON_SIZE)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon_name = icon_name


class Sidebar(QFrame):
    nav_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(200)

        self._buttons: dict[str, _SidebarButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(6)

        title = QLabel("Palisade")
        title.setObjectName("SidebarTitle")
        layout.addWidget(title)
        layout.addSpacing(12)

        for key, label, icon_name in SIDEBAR_ITEMS:
            button = _SidebarButton(label, icon_name)
            button.clicked.connect(lambda _=False, k=key: self.nav_requested.emit(k))
            layout.addWidget(button)
            self._buttons[key] = button

        layout.addStretch(1)

    def set_active_index(self, key: str) -> None:
        for k, button in self._buttons.items():
            button.setChecked(k == key)

    def update_icons_for_theme(self, theme: str) -> None:
        color = "#b4b4bd" if theme == "dark" else "#55555e"
        for button in self._buttons.values():
            button.setIcon(qta.icon(button._icon_name, color=color))
