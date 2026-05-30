from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class FilterCard(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("FilterCard")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(12)

        name = QLabel("Filter Name")
        name.setObjectName("FilterCardName")
        top.addWidget(name, 1)

        self.toggle = QCheckBox()
        self.toggle.setObjectName("FilterCardToggle")
        self.toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        top.addWidget(self.toggle)

        outer.addLayout(top)

        schedule_summary = QLabel("Always")
        schedule_summary.setObjectName("FilterCardSchedule")
        outer.addWidget(schedule_summary)

        blocked_counts = QLabel(f"{1} site {2} apps")
        blocked_counts.setObjectName("FilterCardCounts")
        outer.addWidget(blocked_counts)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        actions.addStretch(1)

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("FilterCardActionButton")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(edit_btn)

        del_btn = QPushButton("Delete")
        del_btn.setObjectName("FilterCardDangerButton")
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(del_btn)

        outer.addLayout(actions)
