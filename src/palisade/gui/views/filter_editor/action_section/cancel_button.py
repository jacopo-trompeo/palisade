from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class CancelButton(QPushButton):
    def __init__(self):
        super().__init__("Cancel")

        self.setObjectName("SecondaryButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
