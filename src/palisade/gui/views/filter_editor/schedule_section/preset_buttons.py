from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class _PresetButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)

        self.setObjectName("PresetButton")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class PresetButtons(QWidget):
    _PRESETS = ["always", "weekdays", "weekends"]
    preset_changed = Signal()

    def __init__(self):
        super().__init__()
        self._buttons: dict[str, _PresetButton] = {}
        self._selected: str | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for key in self._PRESETS:
            button = _PresetButton(key.capitalize())
            button.clicked.connect(lambda checked, k=key: self.apply_preset(k))
            self._buttons[key] = button
            layout.addWidget(button)

        layout.addStretch(1)

    def apply_preset(self, key: str | None):
        self._selected = key
        for k, button in self._buttons.items():
            button.setChecked(k == self._selected)
        self.preset_changed.emit()

    @property
    def selected(self) -> str | None:
        return self._selected
