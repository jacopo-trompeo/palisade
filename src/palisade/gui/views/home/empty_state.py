import qtawesome as qta
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyState(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)
        layout.addStretch(1)

        icon = QLabel()
        icon.setPixmap(
            qta.icon("fa6s.shield-halved", color="#777").pixmap(QSize(64, 64))
        )
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        msg = QLabel("No filters yet - add one to get started.")
        msg.setObjectName("EmptyStateLabel")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)

        layout.addStretch(1)
