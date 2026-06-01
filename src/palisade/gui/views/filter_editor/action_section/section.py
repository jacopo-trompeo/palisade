from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QWidget

from palisade.gui.views.filter_editor.action_section.cancel_button import CancelButton
from palisade.gui.views.filter_editor.action_section.save_button import SaveButton


class ActionSection(QWidget):
    save_requested = Signal()
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addStretch(1)

        save_button = SaveButton()
        save_button.clicked.connect(lambda: self.save_requested.emit())
        cancel_button = CancelButton()
        cancel_button.clicked.connect(lambda: self.cancel_requested.emit())

        layout.addWidget(save_button)
        layout.addWidget(cancel_button)
