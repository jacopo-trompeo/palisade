import qtawesome as qta
from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from palisade import ipc
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

        add_button = PrimaryButton("  Add Filter")
        add_button.setIcon(qta.icon("fa6s.plus", color="#ffffff"))
        add_button.setIconSize(QSize(16, 16))
        add_button.clicked.connect(self.filter_nav_requested.emit)
        header.addWidget(add_button)
        self._root.addLayout(header)

        self._filter_card_list: FilterCardList | None = None
        self.refresh()

    def _delete_filter(self, flt: Filter) -> None:
        if confirm_delete(self, flt.name):
            delete_filter(flt.id)
            ipc.notify({"type": "filters_changed"})
            self.refresh()

    def _edit_filter(self, flt: Filter) -> None:
        self.edit_filter_requested.emit(flt.id)

    def _toggle_filter(self, flt: Filter, enabled: bool) -> None:
        if not enabled and not confirm_disable(self, flt.name):
            self.refresh()
            return
        flt.enabled = enabled
        update_filter(flt)
        ipc.notify({"type": "filters_changed"})

    def _connect_signals(self) -> None:
        if self._filter_card_list is None:
            return
        self._filter_card_list.delete_requested.connect(self._delete_filter)
        self._filter_card_list.edit_requested.connect(self._edit_filter)
        self._filter_card_list.toggle_requested.connect(self._toggle_filter)

    def refresh(self) -> None:
        if self._filter_card_list is not None:
            self._root.removeWidget(self._filter_card_list)
            self._filter_card_list.deleteLater()

        self._filter_card_list = FilterCardList(list_filters())
        self._connect_signals()
        self._root.addWidget(self._filter_card_list, 1)
