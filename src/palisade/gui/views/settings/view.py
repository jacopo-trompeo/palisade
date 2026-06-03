from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from palisade.dbi import set_setting
from palisade.gui.theme import apply_theme, current_theme
from palisade.gui.widgets.section_title import SectionTitle


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(24)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        root.addWidget(SectionTitle("Theme"))

        theme_row = QHBoxLayout()
        theme_row.setSpacing(20)

        self._light = QRadioButton("Light")
        self._light.setCursor(Qt.CursorShape.PointingHandCursor)
        self._dark = QRadioButton("Dark")
        self._dark.setCursor(Qt.CursorShape.PointingHandCursor)

        if current_theme() == "light":
            self._light.setChecked(True)
        else:
            self._dark.setChecked(True)

        group = QButtonGroup(self)
        group.addButton(self._light)
        group.addButton(self._dark)

        self._light.toggled.connect(self._on_theme_changed)
        self._dark.toggled.connect(self._on_theme_changed)

        theme_row.addWidget(self._light)
        theme_row.addWidget(self._dark)
        theme_row.addStretch(1)
        root.addLayout(theme_row)

        root.addStretch(1)

    def _on_theme_changed(self) -> None:
        name = "light" if self._light.isChecked() else "dark"
        set_setting("theme", name)
        apply_theme(name)
