from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QVBoxLayout, QWidget

from palisade.db.models import is_valid_domain
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

        self._website_input = WebsiteInput()
        self._website_input.returnPressed.connect(self.add_website)
        row.addWidget(self._website_input, 1)

        self._add_button = AddButton()
        self._add_button.clicked.connect(self.add_website)
        row.addWidget(self._add_button)

        layout.addLayout(row)

        self._website_chips_holder = QWidget()
        self._website_chips_layout = FlowLayout(self._website_chips_holder, spacing=6)
        layout.addWidget(self._website_chips_holder)

    def add_website(self, website_name: str | None = None) -> None:
        raw = website_name or self._website_input.text().strip().lower()

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

        if raw in self.websites:
            self._website_input.clear()
            return

        self._add_website_chip(raw)
        self._website_input.clear()

    def _add_website_chip(self, domain: str) -> None:
        chip = Chip(domain)
        chip.removed.connect(
            lambda value: remove_chip(self._website_chips_layout, value)
        )
        self._website_chips_layout.addWidget(chip)

    def clear(self) -> None:
        self._website_input.clear()
        for i in range(self._website_chips_layout.count()):
            item = self._website_chips_layout.itemAt(i)
            if item is not None and item.widget() is not None:
                item.widget().deleteLater()

    @property
    def websites(self) -> list[str]:
        return [
            widget.value
            for i in range(self._website_chips_layout.count())
            if (item := self._website_chips_layout.itemAt(i)) is not None
            and (widget := item.widget()) is not None
        ]
