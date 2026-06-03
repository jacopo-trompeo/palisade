from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QVBoxLayout, QWidget

from palisade.db.models import is_valid_domain
from palisade.gui.layout_utils import clear_layout, iter_layout_widgets
from palisade.gui.views.filter_editor.websites_section.add_button import AddButton
from palisade.gui.views.filter_editor.websites_section.website_input import WebsiteInput
from palisade.gui.widgets.chip import Chip, remove_chip
from palisade.gui.widgets.flow_layout import FlowLayout


class WebsitesSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        row = QHBoxLayout()

        self._input = WebsiteInput()
        self._input.returnPressed.connect(self._add_from_input)
        row.addWidget(self._input, 1)

        add_button = AddButton()
        add_button.clicked.connect(self._add_from_input)
        row.addWidget(add_button)

        layout.addLayout(row)

        self._chips_holder = QWidget()
        self._chips_layout = FlowLayout(self._chips_holder, spacing=6)
        layout.addWidget(self._chips_holder)

    def value(self) -> list[str]:
        return [chip.value for chip in iter_layout_widgets(self._chips_layout, Chip)]

    def set_value(self, websites: list[str]) -> None:
        clear_layout(self._chips_layout)
        self._input.clear()
        for website in websites:
            self._add_chip(website)

    def _add_from_input(self) -> None:
        raw = self._input.text().strip().lower()
        if not raw:
            return
        if not is_valid_domain(raw):
            QMessageBox.warning(
                self,
                "Invalid domain",
                f"'{raw}' doesn't look like a domain. "
                "Example: youtube.com — no http://, no paths.",
            )
            return
        if raw in self.value():
            self._input.clear()
            return
        self._add_chip(raw)
        self._input.clear()

    def _add_chip(self, domain: str) -> None:
        chip = Chip(domain)
        chip.removed.connect(lambda value: remove_chip(self._chips_layout, value))
        self._chips_layout.addWidget(chip)
