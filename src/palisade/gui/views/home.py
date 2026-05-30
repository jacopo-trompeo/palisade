from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class HomePage(QWidget):
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
