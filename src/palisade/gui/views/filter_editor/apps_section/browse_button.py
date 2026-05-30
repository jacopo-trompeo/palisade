from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class BrowseButton(QPushButton):
    def __init__(self):
        super().__init__("Browse installed apps")

        self.setObjectName("SecondaryButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
