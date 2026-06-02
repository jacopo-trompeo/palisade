from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

from palisade.db.models import Filter
from palisade.gui.views.home.empty_state import EmptyState
from palisade.gui.views.home.filter_card import FilterCard


class FilterCardList(QWidget):
    delete_requested = Signal(Filter)
    edit_requested = Signal(Filter)
    toggle_requested = Signal(Filter, bool)

    def __init__(self, filters: list[Filter]):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._list_holder = QWidget()
        self._list_layout = QVBoxLayout(self._list_holder)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(12)
        self._list_layout.addStretch(1)

        self._scroll.setWidget(self._list_holder)

        layout.addWidget(self._scroll)

        if not filters:
            self._list_layout.insertWidget(0, EmptyState())
            return

        for filter in filters:
            filter_card = FilterCard(filter)
            filter_card.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
            )
            filter_card.delete_requested.connect(
                lambda filter=filter: self.delete_requested.emit(filter)
            )
            filter_card.edit_requested.connect(
                lambda filter=filter: self.edit_requested.emit(filter)
            )
            filter_card.toggle_requested.connect(
                lambda checked, filter=filter: self.toggle_requested.emit(
                    filter, checked
                )
            )
            self._list_layout.insertWidget(self._list_layout.count() - 1, filter_card)

    @property
    def filter_cards(self) -> list[FilterCard]:
        cards = []
        for i in range(self._list_layout.count() - 1):
            item = self._list_layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if isinstance(widget, FilterCard):
                cards.append(widget)
        return cards
