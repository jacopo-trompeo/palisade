from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class _FilterCardTitle(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setObjectName("FilterCardName")


class _FilterCardToggle(QCheckBox):
    def __init__(self):
        super().__init__()

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
    def __init__(self):
        super().__init__()

        self.setSpacing(8)
        self.addStretch(1)

        edit_button = QPushButton("Edit")
        edit_button.setObjectName("FilterCardActionButton")
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setObjectName("FilterCardDangerButton")
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.addWidget(delete_button)


class FilterCard(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("FilterCard")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(12)

        name = _FilterCardTitle("Filter")
        top.addWidget(name, 1)

        self.toggle = _FilterCardToggle()
        top.addWidget(self.toggle)

        outer.addLayout(top)

        schedule_summary = _FilterCardScheduleSummary("Active Mon-Fri, 9am-5pm")
        outer.addWidget(schedule_summary)

        blocked_counts = _FilterCardBlockedCounts("1 site, 2 apps")
        outer.addWidget(blocked_counts)

        actions = _FilterCardActions()
        outer.addLayout(actions)
