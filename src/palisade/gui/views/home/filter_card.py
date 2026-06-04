import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
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


class FilterCard(QFrame):
    delete_requested = Signal()
    edit_requested = Signal()
    toggle_requested = Signal(bool)

    def __init__(self, flt: Filter):
        super().__init__()

        self.setObjectName("FilterCard")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(12)

        name = _FilterCardTitle(flt.name)
        top.addWidget(name, 1)

        toggle = _FilterCardToggle(flt.enabled)
        toggle.clicked.connect(lambda checked: self.toggle_requested.emit(checked))
        top.addWidget(toggle)

        outer.addLayout(top)

        outer.addWidget(_FilterCardScheduleSummary(flt.schedule.summary()))
        outer.addWidget(_FilterCardBlockedCounts(flt.summary()))
        outer.addLayout(self._build_actions())

    def _build_actions(self) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(8)
        actions.addStretch(1)

        edit_button = QPushButton("  Edit")
        edit_button.setObjectName("FilterCardActionButton")
        edit_button.setIcon(qta.icon("fa6s.pen", color="#87878f"))
        edit_button.setIconSize(QSize(14, 14))
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_button.clicked.connect(self.edit_requested.emit)
        actions.addWidget(edit_button)

        delete_button = QPushButton("  Delete")
        delete_button.setObjectName("FilterCardDangerButton")
        delete_button.setIcon(qta.icon("fa6s.trash", color="#e06060"))
        delete_button.setIconSize(QSize(14, 14))
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.clicked.connect(self.delete_requested.emit)
        actions.addWidget(delete_button)

        return actions
