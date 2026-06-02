import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLayout, QPushButton


def _build_icon(icon: QIcon | QPixmap) -> QLabel:
    label = QLabel()
    if isinstance(icon, QIcon):
        pix = icon.pixmap(QSize(16, 16))
    else:
        pix = icon
    label.setPixmap(pix)
    return label


class _DeleteButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setObjectName("ChipClose")
        self.setIcon(qta.icon("fa6s.xmark", color="#999"))
        self.setIconSize(QSize(12, 12))
        self.setFixedSize(QSize(20, 20))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class Chip(QFrame):
    removed = Signal(str)

    def __init__(
        self,
        value: str,
        label: str | None = None,
        icon: QIcon | QPixmap | None = None,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("Chip")
        self.value = value

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 6, 4)
        layout.setSpacing(6)

        if icon is not None:
            layout.addWidget(_build_icon(icon))

        text = QLabel(label or value)
        text.setObjectName("ChipLabel")
        layout.addWidget(text)

        delete_button = _DeleteButton()
        delete_button.clicked.connect(lambda: self.removed.emit(self.value))
        layout.addWidget(delete_button)


def remove_chip(layout: QLayout, value: str) -> None:
    for i in range(layout.count()):
        item = layout.itemAt(i)
        widget = item.widget() if item else None
        if isinstance(widget, Chip) and widget.value == value:
            layout.takeAt(i)
            widget.deleteLater()
            return
