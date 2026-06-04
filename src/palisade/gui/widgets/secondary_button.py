from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class SecondaryButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)

        self.setObjectName("SecondaryButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
