from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

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

        self._app_input = AppInput()
        self._app_input.returnPressed.connect(self._add_app)
        row.addWidget(self._app_input, 1)

        add_button = AddButton()
        add_button.clicked.connect(self._add_app)
        row.addWidget(add_button)

        browse_button = BrowseButton()
        browse_button.clicked.connect(self._open_app_picker)
        row.addWidget(browse_button)

        layout.addLayout(row)

        self._app_chips_holder = QWidget()
        self._app_chips_layout = FlowLayout(self._app_chips_holder, spacing=6)
        layout.addWidget(self._app_chips_holder)

    def _add_app(self, app_name: str | None = None, icon: QIcon | None = None) -> None:
        raw = app_name or self._app_input.text().strip()
        if not raw:
            return
        if raw in self.apps:
            self._app_input.clear()
            return
        self._add_app_chip(raw, icon)
        self._app_input.clear()

    def _add_app_chip(self, app_name: str, icon: QIcon | None = None) -> None:
        chip = Chip(app_name, icon=icon)
        chip.removed.connect(
            lambda value: remove_chip(self._app_chips_layout, value)
        )
        self._app_chips_layout.addWidget(chip)

    def _open_app_picker(self) -> None:
        dlg = AppPickerDialog(self)
        if dlg.exec():
            for app in dlg.picked:
                if app.exec_name in self.apps:
                    continue
                icon = QIcon.fromTheme(app.icon) if app.icon else None
                self._add_app(app.exec_name, icon)

    @property
    def apps(self) -> list[str]:
        return [
            widget.value
            for i in range(self._app_chips_layout.count())
            if (item := self._app_chips_layout.itemAt(i)) is not None
            and (widget := item.widget()) is not None
        ]
