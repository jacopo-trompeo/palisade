from PySide6.QtWidgets import QVBoxLayout, QWidget

from palisade.gui.views.filter_editor.schedule_section.day_picker import DayPicker
from palisade.gui.views.filter_editor.schedule_section.preset_buttons import (
    PresetButtons,
)
from palisade.gui.views.filter_editor.schedule_section.time_range_row import (
    TimeRangeRow,
)


class ScheduleSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        layout.addWidget(PresetButtons())
        layout.addWidget(DayPicker())
        layout.addWidget(TimeRangeRow())
