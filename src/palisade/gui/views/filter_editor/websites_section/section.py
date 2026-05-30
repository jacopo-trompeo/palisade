from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from palisade.gui.views.filter_editor.websites_section.add_button import AddButton
from palisade.gui.views.filter_editor.websites_section.website_input import WebsiteInput


class WebsitesSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        row = QHBoxLayout()

        row.addWidget(WebsiteInput(), 1)
        row.addWidget(AddButton())

        layout.addLayout(row)
