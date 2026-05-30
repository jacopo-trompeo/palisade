from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.widgets.section_title import SectionTitle


class _PresetButtons(QWidget):
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


class _DayPicker(QWidget):
    DAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    def __init__(self):
        super().__init__()

        day_row = QHBoxLayout(self)
        day_row.setSpacing(6)

        for label in self.DAY_LABELS:
            button = self._make_day_button(label)
            day_row.addWidget(button)

        day_row.addStretch(1)

    def _make_day_button(self, key: str):
        button = QPushButton(key)
        button.setObjectName("DayButton")
        button.setCheckable(True)
        button.setFixedSize(QSize(40, 40))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button


class FilterEditorView(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        body = QWidget()
        root.addWidget(body)
        layout = QVBoxLayout(body)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        self._title_label = QLabel("Add Filter")
        self._title_label.setObjectName("PageTitle")
        layout.addWidget(self._title_label)

        layout.addWidget(SectionTitle("Name"))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Filter name...")
        self._name_input.setObjectName("LargeInput")
        layout.addWidget(self._name_input)

        layout.addWidget(SectionTitle("Schedule"))
        layout.addLayout(self._build_schedule_section())

    def _build_schedule_section(self) -> QVBoxLayout:
        wrap = QVBoxLayout()
        wrap.setSpacing(12)

        wrap.addWidget(_PresetButtons())
        wrap.addWidget(_DayPicker())

        return wrap
