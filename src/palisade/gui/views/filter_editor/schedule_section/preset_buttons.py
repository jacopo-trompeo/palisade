from enum import StrEnum

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class Preset(StrEnum):
    ALWAYS = "always"
    WEEKDAYS = "weekdays"
    WEEKENDS = "weekends"


class _PresetButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)

        self.setObjectName("PresetButton")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class PresetButtons(QWidget):
    preset_changed = Signal()

    def __init__(self):
        super().__init__()
        self._buttons: dict[Preset, _PresetButton] = {}
        self._selected: Preset | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for preset in Preset:
            button = _PresetButton(preset.capitalize())
            button.clicked.connect(lambda checked, p=preset: self.apply_preset(p))
            self._buttons[preset] = button
            layout.addWidget(button)

        layout.addStretch(1)

    def apply_preset(self, preset: Preset | None) -> None:
        self._selected = Preset(preset) if preset is not None else None
        for key, button in self._buttons.items():
            button.setChecked(key == self._selected)
        self.preset_changed.emit()

    @property
    def selected(self) -> Preset | None:
        return self._selected
