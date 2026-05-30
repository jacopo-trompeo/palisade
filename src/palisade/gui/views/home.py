from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


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
        root.addLayout(header)
