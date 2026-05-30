from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.views.home.filter_card_list import FilterCardList
from palisade.gui.widgets.primary_button import PrimaryButton


class HomeView(QWidget):
    filter_nav_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(20)

        header = QHBoxLayout()
        label = QLabel("Home")
        label.setObjectName("HomeLabel")
        header.addWidget(label)
        root.addLayout(header)

        add_button = PrimaryButton("Add Filter")
        add_button.clicked.connect(self.filter_nav_requested.emit)
        header.addWidget(add_button)

        root.addWidget(FilterCardList(), 1)
