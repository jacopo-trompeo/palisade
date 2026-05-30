from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class _PresetButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)

        self.setObjectName("PresetButton")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class PresetButtons(QWidget):
    PRESETS = ["always", "weekdays", "weekends"]

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for key in self.PRESETS:
            button = _PresetButton(key.capitalize())
            layout.addWidget(button)

        layout.addStretch(1)
