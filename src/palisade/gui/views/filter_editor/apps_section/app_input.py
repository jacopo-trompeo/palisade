from PySide6.QtWidgets import QLineEdit


class AppInput(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setPlaceholderText("process name (e.g. discord)")
