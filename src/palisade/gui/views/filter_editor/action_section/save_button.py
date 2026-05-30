from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class SaveButton(QPushButton):
    def __init__(self):
        super().__init__("Save")

        self.setObjectName("PrimaryButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
