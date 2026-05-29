from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from palisade.config import DEV_MODE
from palisade.gui.widgets.dev_banner import DevBanner


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palisade")
        self.resize(960, 640)

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        if DEV_MODE:
            root_layout.addWidget(DevBanner())

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        root_layout.addWidget(body, 1)
