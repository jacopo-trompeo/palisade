from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class AboutView(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(20)

        header = QHBoxLayout()
        label = QLabel("About")
        label.setObjectName("AboutLabel")
        header.addWidget(label)
        root.addLayout(header)
