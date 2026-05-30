from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.views.filter_editor.day_picker import _DayPicker
from palisade.gui.views.filter_editor.preset_buttons import _PresetButtons
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

    def _build_schedule_section(self) -> QVBoxLayout:
        wrap = QVBoxLayout()
        wrap.setSpacing(12)

        wrap.addWidget(_PresetButtons())
        wrap.addWidget(_DayPicker())

        return wrap
