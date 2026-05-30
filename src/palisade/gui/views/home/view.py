from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.views.home.filter_card import FilterCard


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

        add_btn = QPushButton("Add Filter")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.filter_nav_requested.emit)
        header.addWidget(add_btn)

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

        for _ in range(3):
            card = FilterCard()
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self._list_layout.insertWidget(self._list_layout.count() - 1, card)

        root.addWidget(self._scroll, 1)
