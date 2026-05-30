import qtawesome as qta
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)


class _TimeInput(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setObjectName("TimeInput")
        self.setInputMask("99:99")
        self.setMaxLength(5)
        self.setFixedWidth(80)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("00:00")


class _RemoveButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setObjectName("IconButton")
        self.setIcon(qta.icon("fa6s.xmark", color="#999"))
        self.setIconSize(QSize(14, 14))
        self.setFixedSize(QSize(28, 28))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class TimeRangeRow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._start = _TimeInput()
        self._end = _TimeInput()

        layout.addWidget(self._start)

        dash = QLabel("–")
        dash.setObjectName("TimeRangeDash")

        layout.addWidget(dash)
        layout.addWidget(self._end)
        layout.addWidget(_RemoveButton())

        layout.addStretch(1)
