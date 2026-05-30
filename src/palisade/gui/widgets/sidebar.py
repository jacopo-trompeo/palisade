from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

SIDEBAR_ITEMS = [
    ("home", "Home"),
    ("settings", "Settings"),
    ("about", "About"),
]


class Sidebar(QFrame):
    nav_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(200)
        self._buttons: dict[str, QPushButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(6)

        title = QLabel("Palisade")
        title.setObjectName("SidebarTitle")
        layout.addWidget(title)
        layout.addSpacing(12)

        for key, label in SIDEBAR_ITEMS:
            btn = QPushButton(f"{label}")
            btn.setObjectName("SidebarButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(
                lambda _checked=False, k=key: self._on_nav_item_click(k)
            )
            layout.addWidget(btn)
            self._buttons[key] = btn

        layout.addStretch(1)

    def _on_nav_item_click(self, key: str) -> None:
        self._set_active_index(key)
        self.nav_requested.emit(key)

    def _set_active_index(self, key: str) -> None:
        for k, btn in self._buttons.items():
            btn.setChecked(k == key)
