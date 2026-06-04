from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from palisade import __version__


class AboutView(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(16)
        root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        name = QLabel("Palisade")
        name.setObjectName("AboutAppName")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(name)

        version = QLabel(f"Version {__version__}")
        version.setObjectName("AboutAppVersion")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(version)

        description = QLabel("Block distracting websites and apps on a schedule.")
        description.setObjectName("AboutAppDescription")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        root.addWidget(description)

        creator = QLabel("Created by Jacopo Trompeo")
        creator.setObjectName("AboutAppCreator")
        creator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        root.addWidget(creator)
