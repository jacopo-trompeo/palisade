from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from palisade.dbi import (
    EDIT_LOCK_SECONDS_MAX,
    EDIT_LOCK_SECONDS_MIN,
    get_edit_lock_seconds,
    set_edit_lock_seconds,
    set_setting,
)
from palisade.gui.theme import apply_theme, current_theme
from palisade.gui.widgets.section_title import SectionTitle


class SettingsView(QWidget):
    theme_changed = Signal(str)

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

        root.addWidget(SectionTitle("Edit-lock duration"))

        help_text = QLabel(
            "How long the filter editor stays read-only after you click Edit. "
            "Longer durations make it harder to quickly unblock yourself in a "
            "moment of weakness."
        )
        help_text.setObjectName("SettingsHelpText")
        help_text.setWordWrap(True)
        root.addWidget(help_text)

        lock_row = QHBoxLayout()
        lock_row.setSpacing(10)
        self._lock_input = QLineEdit()
        self._lock_input.setObjectName("DurationInput")
        self._lock_input.setValidator(
            QIntValidator(EDIT_LOCK_SECONDS_MIN, EDIT_LOCK_SECONDS_MAX, self)
        )
        self._lock_input.setMaxLength(3)
        self._lock_input.setFixedWidth(80)
        self._lock_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lock_input.setText(str(get_edit_lock_seconds()))
        self._lock_input.editingFinished.connect(self._commit_lock_value)
        lock_row.addWidget(self._lock_input)
        lock_row.addWidget(QLabel("seconds"))
        lock_row.addWidget(
            QLabel(f"  (between {EDIT_LOCK_SECONDS_MIN} and {EDIT_LOCK_SECONDS_MAX})")
        )
        lock_row.addStretch(1)
        root.addLayout(lock_row)

        root.addStretch(1)

    def _on_theme_changed(self) -> None:
        name = "light" if self._light.isChecked() else "dark"
        set_setting("theme", name)
        apply_theme(name)
        self.theme_changed.emit(name)

    def _commit_lock_value(self) -> None:
        try:
            v = int(self._lock_input.text())
        except ValueError:
            v = get_edit_lock_seconds()
        set_edit_lock_seconds(v)
        clamped = get_edit_lock_seconds()
        if str(clamped) != self._lock_input.text():
            self._lock_input.setText(str(clamped))
