from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from palisade.gui.layout_utils import clear_layout, iter_layout_widgets
from palisade.gui.views.filter_editor.apps_section.add_button import AddButton
from palisade.gui.views.filter_editor.apps_section.app_input import AppInput
from palisade.gui.views.filter_editor.apps_section.browse_button import BrowseButton
from palisade.gui.widgets.app_picker import AppPickerDialog
from palisade.gui.widgets.chip import Chip, remove_chip
from palisade.gui.widgets.flow_layout import FlowLayout


class AppsSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        row = QHBoxLayout()

        self._input = AppInput()
        self._input.returnPressed.connect(self._add_from_input)
        row.addWidget(self._input, 1)

        add_button = AddButton()
        add_button.clicked.connect(self._add_from_input)
        row.addWidget(add_button)

        browse_button = BrowseButton()
        browse_button.clicked.connect(self._open_app_picker)
        row.addWidget(browse_button)

        layout.addLayout(row)

        self._chips_holder = QWidget()
        self._chips_layout = FlowLayout(self._chips_holder, spacing=6)
        layout.addWidget(self._chips_holder)

    def value(self) -> list[str]:
        return [chip.value for chip in iter_layout_widgets(self._chips_layout, Chip)]

    def set_value(self, apps: list[str]) -> None:
        clear_layout(self._chips_layout)
        self._input.clear()
        for app in apps:
            self._add_chip(app)

    def _add_from_input(self) -> None:
        raw = self._input.text().strip()
        if not raw:
            return
        self._add(raw)
        self._input.clear()

    def _add(self, app_name: str, icon: QIcon | None = None) -> None:
        if app_name in self.value():
            return
        self._add_chip(app_name, icon)

    def _add_chip(self, app_name: str, icon: QIcon | None = None) -> None:
        chip = Chip(app_name, icon=icon)
        chip.removed.connect(lambda value: remove_chip(self._chips_layout, value))
        self._chips_layout.addWidget(chip)

    def _open_app_picker(self) -> None:
        dlg = AppPickerDialog(self)
        if dlg.exec():
            for app in dlg.picked:
                icon = QIcon.fromTheme(app.icon) if app.icon else None
                self._add(app.exec_name, icon)
