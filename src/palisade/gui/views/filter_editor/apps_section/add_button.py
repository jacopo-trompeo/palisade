from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class AddButton(QPushButton):
    def __init__(self):
        super().__init__("Add")

        self.setObjectName("SecondaryButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
