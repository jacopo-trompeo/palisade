from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from palisade.db.models import Schedule, ScheduleType, TimeRange
from palisade.gui.layout_utils import clear_layout, iter_layout_widgets
from palisade.gui.views.filter_editor.schedule_section.day_picker import DayPicker
from palisade.gui.views.filter_editor.schedule_section.preset_buttons import (
    Preset,
    PresetButtons,
)
from palisade.gui.views.filter_editor.schedule_section.time_range_row import (
    TimeRangeRow,
)

_WEEKDAYS = {0, 1, 2, 3, 4}
_WEEKENDS = {5, 6}
_FULL_DAY = TimeRange("00:00", "23:59")


class _AddRangeButton(QPushButton):
    def __init__(self):
        super().__init__("Add time range")
        self.setObjectName("LinkButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class ScheduleSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self._preset_buttons = PresetButtons()
        self._preset_buttons.preset_changed.connect(self._on_preset_changed)

        self._detail_panel = QWidget()
        detail = QVBoxLayout(self._detail_panel)
        detail.setContentsMargins(0, 0, 0, 0)
        detail.setSpacing(10)

        self._day_picker = DayPicker()
        self._day_picker.toggled.connect(self._sync_preset_from_state)

        self._ranges_container = QVBoxLayout()
        self._ranges_container.setSpacing(6)

        detail.addWidget(self._day_picker)
        detail.addLayout(self._ranges_container)

        add_range_button = _AddRangeButton()
        add_range_button.clicked.connect(lambda: self._add_time_range(None))
        detail.addWidget(add_range_button, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self._preset_buttons)
        layout.addWidget(self._detail_panel)

    def value(self) -> Schedule:
        if self._preset_buttons.selected == Preset.ALWAYS:
            return Schedule(type=ScheduleType.ALWAYS)
        return Schedule(
            type=ScheduleType.CUSTOM,
            days=sorted(self._day_picker.selected_days),
            time_ranges=self._time_ranges,
        )

    def set_value(self, schedule: Schedule) -> None:
        self._clear()
        if schedule.type == ScheduleType.ALWAYS:
            self._add_time_range(None)
            return
        self._day_picker.set_days(set(schedule.days))
        for time_range in schedule.time_ranges:
            self._add_time_range(time_range)
        if not schedule.time_ranges:
            self._add_time_range(None)
        self._sync_preset_from_state()

    def _clear(self) -> None:
        self._preset_buttons.apply_preset(Preset.ALWAYS)
        self._day_picker.set_days(set())
        clear_layout(self._ranges_container)

    def _on_preset_changed(self) -> None:
        selected = self._preset_buttons.selected
        if selected == Preset.ALWAYS:
            self._detail_panel.setVisible(False)
        else:
            self._detail_panel.setVisible(True)
            if selected == Preset.WEEKDAYS:
                self._day_picker.set_days(_WEEKDAYS)
            elif selected == Preset.WEEKENDS:
                self._day_picker.set_days(_WEEKENDS)

    def _sync_preset_from_state(self) -> None:
        days = set(self._day_picker.selected_days)
        full_day = self._time_ranges == [_FULL_DAY]
        matched: Preset | None = None
        if days == _WEEKDAYS and full_day:
            matched = Preset.WEEKDAYS
        elif days == _WEEKENDS and full_day:
            matched = Preset.WEEKENDS
        self._preset_buttons.apply_preset(matched)

    def _add_time_range(self, time_range: TimeRange | None) -> None:
        row = TimeRangeRow(time_range)
        row.removed.connect(self._remove_time_range)
        row.changed.connect(self._sync_preset_from_state)
        self._ranges_container.addWidget(row)
        self._update_range_remove_buttons()

    def _remove_time_range(self, row: TimeRangeRow) -> None:
        self._ranges_container.removeWidget(row)
        row.deleteLater()
        self._update_range_remove_buttons()
        self._sync_preset_from_state()

    def _update_range_remove_buttons(self) -> None:
        rows = iter_layout_widgets(self._ranges_container, TimeRangeRow)
        single = len(rows) <= 1
        for row in rows:
            row.set_remove_button_visible(not single)

    @property
    def _time_ranges(self) -> list[TimeRange]:
        return [
            row.value()
            for row in iter_layout_widgets(self._ranges_container, TimeRangeRow)
        ]
