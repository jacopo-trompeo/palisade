from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

from palisade.db.models import Filter
from palisade.gui.layout_utils import iter_layout_widgets
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

        for flt in filters:
            card = FilterCard(flt)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            card.delete_requested.connect(
                lambda flt=flt: self.delete_requested.emit(flt)
            )
            card.edit_requested.connect(lambda flt=flt: self.edit_requested.emit(flt))
            card.toggle_requested.connect(
                lambda checked, flt=flt: self.toggle_requested.emit(flt, checked)
            )
            self._list_layout.insertWidget(self._list_layout.count() - 1, card)

    @property
    def filter_cards(self) -> list[FilterCard]:
        return iter_layout_widgets(self._list_layout, FilterCard)
