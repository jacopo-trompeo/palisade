from PySide6.QtWidgets import QLabel


class SectionTitle(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName("SectionTitle")
