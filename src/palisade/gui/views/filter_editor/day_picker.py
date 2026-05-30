from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class DayPicker(QWidget):
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
