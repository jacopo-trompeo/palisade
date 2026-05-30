from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.views.filter_editor.day_picker import DayPicker
from palisade.gui.views.filter_editor.preset_buttons import PresetButtons
from palisade.gui.views.filter_editor.time_range_row import TimeRangeRow
from palisade.gui.widgets.section_title import SectionTitle


class FilterEditorView(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        body = QWidget()
        root.addWidget(body)
        layout = QVBoxLayout(body)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        self._title_label = QLabel("Add Filter")
        self._title_label.setObjectName("PageTitle")
        layout.addWidget(self._title_label)

        layout.addWidget(SectionTitle("Name"))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Filter name...")
        self._name_input.setObjectName("LargeInput")
        layout.addWidget(self._name_input)

        layout.addWidget(SectionTitle("Schedule"))
        layout.addLayout(self._build_schedule_section())

        layout.addWidget(SectionTitle("Blocked Websites"))
        layout.addLayout(self._build_websites_section())

        layout.addWidget(SectionTitle("Blocked apps"))
        layout.addLayout(self._build_apps_section())

    def _build_schedule_section(self) -> QVBoxLayout:
        wrap = QVBoxLayout()
        wrap.setSpacing(12)

        wrap.addWidget(PresetButtons())
        wrap.addWidget(DayPicker())
        wrap.addWidget(TimeRangeRow())

        return wrap

    def _build_websites_section(self) -> QVBoxLayout:
        wrap = QVBoxLayout()
        wrap.setSpacing(8)

        row = QHBoxLayout()

        self._website_input = QLineEdit()
        self._website_input.setPlaceholderText("example.com")

        row.addWidget(self._website_input, 1)

        add_button = QPushButton("Add")
        add_button.setObjectName("SecondaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)

        row.addWidget(add_button)
        wrap.addLayout(row)

        return wrap

    def _build_apps_section(self) -> QVBoxLayout:
        wrap = QVBoxLayout()
        wrap.setSpacing(8)

        row = QHBoxLayout()

        self._app_input = QLineEdit()
        self._app_input.setPlaceholderText("process name (e.g. discord)")

        row.addWidget(self._app_input, 1)

        add_button = QPushButton("Add")
        add_button.setObjectName("SecondaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)

        row.addWidget(add_button)

        browse_button = QPushButton("Browse installed apps")
        browse_button.setObjectName("SecondaryButton")
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)

        row.addWidget(browse_button)
        wrap.addLayout(row)

        return wrap
