from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class _DayButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)

        self.setObjectName("DayButton")
        self.setCheckable(True)
        self.setFixedSize(QSize(40, 40))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class DayPicker(QWidget):
    DAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    def __init__(self):
        super().__init__()

        day_row = QHBoxLayout(self)
        day_row.setContentsMargins(0, 0, 0, 0)
        day_row.setSpacing(6)

        for label in self.DAY_LABELS:
            button = _DayButton(label)
            day_row.addWidget(button)

        day_row.addStretch(1)
