from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from palisade.gui.layout_utils import iter_layout_widgets


class _DayButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)

        self.setObjectName("DayButton")
        self.setCheckable(True)
        self.setFixedSize(QSize(40, 40))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class DayPicker(QWidget):
    _DAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    toggled = Signal()

    def __init__(self):
        super().__init__()
        self._selected_days: set[int] = set()

        day_row = QHBoxLayout(self)
        day_row.setContentsMargins(0, 0, 0, 0)
        day_row.setSpacing(6)

        for i, label in enumerate(self._DAY_LABELS):
            button = _DayButton(label)
            button.clicked.connect(lambda checked, idx=i: self.toggle_day(checked, idx))
            day_row.addWidget(button)

        day_row.addStretch(1)

    def toggle_day(self, checked: bool, day_index: int):
        if checked:
            self._selected_days.add(day_index)
        else:
            self._selected_days.discard(day_index)
        self.toggled.emit()

    def set_days(self, days: set[int]):
        self._selected_days = set(days)
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i in days)

    @property
    def selected_days(self) -> frozenset[int]:
        return frozenset(self._selected_days)

    @property
    def _buttons(self) -> list[_DayButton]:
        layout = self.layout()
        if layout is None:
            return []
        return iter_layout_widgets(layout, _DayButton)
