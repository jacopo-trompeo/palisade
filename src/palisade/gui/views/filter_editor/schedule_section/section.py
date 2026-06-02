from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from palisade.db.models import TimeRange
from palisade.gui.views.filter_editor.schedule_section.day_picker import DayPicker
from palisade.gui.views.filter_editor.schedule_section.preset_buttons import (
    PresetButtons,
)
from palisade.gui.views.filter_editor.schedule_section.time_range_row import (
    TimeRangeRow,
)


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

        self.preset_buttons = PresetButtons()
        self.preset_buttons.preset_changed.connect(self._set_date_time_visible)

        self._detail_panel = QWidget()
        detail = QVBoxLayout(self._detail_panel)
        detail.setContentsMargins(0, 0, 0, 0)
        detail.setSpacing(10)

        self.day_picker = DayPicker()
        self.day_picker.toggled.connect(self._sync_preset_from_state)

        self._ranges_container = QVBoxLayout()
        self._ranges_container.setSpacing(6)

        detail.addWidget(self.day_picker)
        detail.addLayout(self._ranges_container)

        add_range_button = _AddRangeButton()
        add_range_button.clicked.connect(lambda: self._add_time_range(None))
        detail.addWidget(add_range_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self._add_time_range(None)

        layout.addWidget(self.preset_buttons)
        layout.addWidget(self._detail_panel)

    def _set_date_time_visible(self):
        selected = self.preset_buttons.selected
        if selected == "always":
            self._detail_panel.setVisible(False)
        else:
            self._detail_panel.setVisible(True)

            if selected == "weekdays":
                self.day_picker.set_days({0, 1, 2, 3, 4})
            elif selected == "weekends":
                self.day_picker.set_days({5, 6})

    def _sync_preset_from_state(self) -> None:
        days = self.day_picker.selected_days
        ranges = self.time_ranges
        full_day = ranges == [TimeRange("00:00", "23:59")]
        matched: str | None = None
        if days == {0, 1, 2, 3, 4} and full_day:
            matched = "weekdays"
        elif days == {5, 6} and full_day:
            matched = "weekends"
        self.preset_buttons.apply_preset(matched)

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
        rows = [
            widget
            for i in range(self._ranges_container.count())
            if (item := self._ranges_container.itemAt(i)) is not None
            and (widget := item.widget()) is not None
        ]
        single = len(rows) <= 1
        for r in rows:
            if isinstance(r, TimeRangeRow):
                r.set_remove_button_visible(not single)

    @property
    def time_ranges(self) -> list[TimeRange]:
        return [
            widget.value()
            for i in range(self._ranges_container.count())
            if (item := self._ranges_container.itemAt(i)) is not None
            and (widget := item.widget()) is not None
            and isinstance(widget, TimeRangeRow)
        ]
