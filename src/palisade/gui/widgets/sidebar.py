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
                lambda _checked=False, k=key: self.nav_requested.emit(k)
            )
            layout.addWidget(btn)
            self._buttons[key] = btn

        layout.addStretch(1)

    def set_active_index(self, key: str) -> None:
        for k, btn in self._buttons.items():
            btn.setChecked(k == key)
