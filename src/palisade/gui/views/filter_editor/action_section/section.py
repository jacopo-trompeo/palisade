from PySide6.QtWidgets import QHBoxLayout, QWidget

from palisade.gui.views.filter_editor.action_section.cancel_button import CancelButton
from palisade.gui.views.filter_editor.action_section.save_button import SaveButton


class ActionSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addStretch(1)

        layout.addWidget(CancelButton())
        layout.addWidget(SaveButton())
