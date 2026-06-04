from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
)


class DevBanner(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("DevBanner")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)

        label = QLabel("DEV MODE - no system changes are being made")
        label.setObjectName("DevBannerLabel")
        layout.addWidget(label)

        layout.addStretch(1)
