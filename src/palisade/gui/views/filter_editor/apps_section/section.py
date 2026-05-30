from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from palisade.gui.views.filter_editor.apps_section.add_button import AddButton
from palisade.gui.views.filter_editor.apps_section.app_input import AppInput
from palisade.gui.views.filter_editor.apps_section.browse_button import BrowseButton


class AppsSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        row = QHBoxLayout()

        row.addWidget(AppInput(), 1)
        row.addWidget(AddButton())
        row.addWidget(BrowseButton())

        layout.addLayout(row)
