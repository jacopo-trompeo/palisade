from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class PresetButtons(QWidget):
    PRESETS = ["always", "weekdays", "weekends"]

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setSpacing(8)

        for key in self.PRESETS:
            button = self._make_preset_btn(key)
            layout.addWidget(button)

        layout.addStretch(1)

    def _make_preset_btn(self, key: str) -> QPushButton:
        button = QPushButton(key.capitalize())
        button.setObjectName("PresetButton")
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button
