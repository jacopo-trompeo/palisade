from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from palisade.db.database import list_filters
from palisade.gui.views.home.filter_card_list import FilterCardList
from palisade.gui.widgets.primary_button import PrimaryButton


class HomeView(QWidget):
    filter_nav_requested = Signal()

    def __init__(self):
        super().__init__()

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(32, 28, 32, 28)
        self._root.setSpacing(20)

        header = QHBoxLayout()

        label = QLabel("Home")
        label.setObjectName("PageTitle")
        header.addWidget(label)

        header.addStretch(1)

        add_button = PrimaryButton("Add Filter")
        add_button.clicked.connect(self.filter_nav_requested.emit)
        header.addWidget(add_button)
        self._root.addLayout(header)

        self._filter_card_list: FilterCardList | None = None
        self.refresh()

    def refresh(self) -> None:
        if self._filter_card_list is not None:
            self._root.removeWidget(self._filter_card_list)
            self._filter_card_list.deleteLater()

        # TODO: show a dedicated empty state when there are no filters
        self._filter_card_list = FilterCardList(list_filters())
        self._root.addWidget(self._filter_card_list, 1)
