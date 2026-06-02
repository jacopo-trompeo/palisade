from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from palisade.db.models import Filter


class _FilterCardTitle(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setObjectName("FilterCardName")


class _FilterCardToggle(QCheckBox):
    def __init__(self, checked: bool):
        super().__init__()

        self.setChecked(checked)
        self.setObjectName("FilterCardToggle")


class _FilterCardScheduleSummary(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setObjectName("FilterCardSchedule")


class _FilterCardBlockedCounts(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setObjectName("FilterCardCounts")


class _FilterCardActions(QHBoxLayout):
    delete_requested = Signal()
    edit_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setSpacing(8)
        self.addStretch(1)

        edit_button = QPushButton("Edit")
        edit_button.setObjectName("FilterCardActionButton")
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_button.clicked.connect(self.edit_requested.emit)
        self.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setObjectName("FilterCardDangerButton")
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.clicked.connect(self.delete_requested.emit)
        self.addWidget(delete_button)


class FilterCard(QFrame):
    delete_requested = Signal()
    edit_requested = Signal()
    toggle_requested = Signal(bool)

    def __init__(self, filter: Filter):
        super().__init__()

        self.setObjectName("FilterCard")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(12)

        name = _FilterCardTitle(filter.name)
        top.addWidget(name, 1)

        toggle = _FilterCardToggle(filter.enabled)
        toggle.clicked.connect(lambda checked: self.toggle_requested.emit(checked))
        top.addWidget(toggle)

        outer.addLayout(top)

        schedule_summary = _FilterCardScheduleSummary(filter.schedule.summary())
        outer.addWidget(schedule_summary)

        blocked_counts = _FilterCardBlockedCounts(filter.summary())
        outer.addWidget(blocked_counts)

        actions = _FilterCardActions()
        actions.delete_requested.connect(self.delete_requested.emit)
        actions.edit_requested.connect(self.edit_requested.emit)
        outer.addLayout(actions)
