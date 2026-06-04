from PySide6.QtWidgets import QLineEdit


class WebsiteInput(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setPlaceholderText("example.com")
