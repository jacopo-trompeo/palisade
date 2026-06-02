import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from palisade.db.models import TimeRange


def _normalize_time(s: str) -> str:
    try:
        h_str, m_str = s.split(":")
        h = max(0, min(23, int(h_str)))
        m = max(0, min(59, int(m_str)))
        return f"{h:02d}:{m:02d}"
    except ValueError, IndexError:
        return "00:00"


class _TimeInput(QLineEdit):
    def __init__(self, initial: str):
        super().__init__()

        self.setObjectName("TimeInput")
        self.setInputMask("99:99")
        self.setMaxLength(5)
        self.setFixedWidth(80)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText(initial)


class _RemoveButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setObjectName("IconButton")
        self.setIcon(qta.icon("fa6s.xmark", color="#999"))
        self.setIconSize(QSize(14, 14))
        self.setFixedSize(QSize(28, 28))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class TimeRangeRow(QWidget):
    removed = Signal(object)
    changed = Signal()

    def __init__(self, time_range: TimeRange | None = None):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        start_val = time_range.start if time_range is not None else "00:00"
        end_val = time_range.end if time_range is not None else "23:59"

        self._start = _TimeInput(start_val)
        self._end = _TimeInput(end_val)
        self._start.textChanged.connect(lambda: self.changed.emit())
        self._end.textChanged.connect(lambda: self.changed.emit())

        layout.addWidget(self._start)

        dash = QLabel("–")
        dash.setObjectName("TimeRangeDash")

        layout.addWidget(dash)
        layout.addWidget(self._end)

        self._remove_button = _RemoveButton()
        self._remove_button.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(self._remove_button)

        layout.addStretch(1)

    def value(self) -> TimeRange:
        return TimeRange(
            start=_normalize_time(self._start.text()),
            end=_normalize_time(self._end.text()),
        )

    def set_remove_button_visible(self, visible: bool) -> None:
        self._remove_button.setVisible(visible)
