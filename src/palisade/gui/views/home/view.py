from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from palisade.db.database import delete_filter, list_filters, update_filter
from palisade.db.models import Filter
from palisade.gui.views.home.filter_card_list import FilterCardList
from palisade.gui.widgets.confirm_dialog import confirm_delete, confirm_disable
from palisade.gui.widgets.primary_button import PrimaryButton


class HomeView(QWidget):
    filter_nav_requested = Signal()
    edit_filter_requested = Signal(str)

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

    def _delete_filter(self, filter: Filter) -> None:
        if confirm_delete(self, filter.name):
            delete_filter(filter.id)
            self.refresh()

    def _edit_filter(self, filter: Filter) -> None:
        self.edit_filter_requested.emit(filter.id)

    def _toggle_filter(self, filter: Filter, enabled: bool) -> None:
        filter.enabled = enabled
        if filter.enabled:
            update_filter(filter)
        else:
            if confirm_disable(self, filter.name):
                update_filter(filter)

    def _connect_signals(self) -> None:
        if self._filter_card_list is None:
            return
        self._filter_card_list.delete_requested.connect(
            lambda filter: self._delete_filter(filter)
        )
        self._filter_card_list.edit_requested.connect(
            lambda filter: self._edit_filter(filter)
        )
        self._filter_card_list.toggle_requested.connect(
            lambda filter, checked: self._toggle_filter(filter, checked)
        )

    def refresh(self) -> None:
        if self._filter_card_list is not None:
            self._root.removeWidget(self._filter_card_list)
            self._filter_card_list.deleteLater()

        self._filter_card_list = FilterCardList(list_filters())
        self._connect_signals()
        self._root.addWidget(self._filter_card_list, 1)
