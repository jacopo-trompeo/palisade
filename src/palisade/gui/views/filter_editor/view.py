from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from palisade.db.database import create_filter
from palisade.db.models import Filter, Schedule
from palisade.gui.views.filter_editor.action_section import ActionSection
from palisade.gui.views.filter_editor.apps_section import AppsSection
from palisade.gui.views.filter_editor.schedule_section import ScheduleSection
from palisade.gui.views.filter_editor.websites_section import WebsitesSection
from palisade.gui.widgets.section_title import SectionTitle


class FilterEditorView(QWidget):
    save_requested = Signal()

    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window

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
        self._name_input.setObjectName("FilterInput")
        layout.addWidget(self._name_input)

        layout.addWidget(SectionTitle("Schedule"))
        self._schedule_section = ScheduleSection()
        self._schedule_section.preset_buttons.apply_preset("always")
        layout.addWidget(self._schedule_section)

        layout.addWidget(SectionTitle("Blocked Websites"))
        self._website_section = WebsitesSection()
        layout.addWidget(self._website_section)

        layout.addWidget(SectionTitle("Blocked apps"))
        self._apps_section = AppsSection()
        layout.addWidget(self._apps_section)

        layout.addSpacing(8)

        actions = ActionSection()
        actions.cancel_requested.connect(self._on_cancel)
        actions.save_requested.connect(self._on_save)
        layout.addWidget(actions)

        layout.addStretch(1)

    def _on_cancel(self):
        self._main_window.navigate("home")

    def _on_save(self):
        name = self._name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Name required", "Please give the filter a name.")
            return

        selected_preset = self._schedule_section.preset_buttons.selected
        if selected_preset == "always":
            schedule = Schedule(type="always")
        else:
            days = self._schedule_section.day_picker.selected_days
            if not days:
                QMessageBox.warning(self, "No days selected", "Pick at least one day.")
                return
            ranges = self._schedule_section.time_ranges
            if not ranges:
                QMessageBox.warning(
                    self, "No time range", "Add at least one time range."
                )
                return
            schedule = Schedule(type="custom", days=list(days), time_ranges=ranges)

        websites = self._website_section.websites
        apps = self._apps_section.apps

        f = Filter(
            name=name,
            schedule=schedule,
            blocked_websites=websites,
            blocked_apps=apps,
            enabled=True,
        )
        create_filter(f)

        self._clear_form()
        self._main_window.navigate("home")
        self.save_requested.emit()

    def _clear_form(self):
        self._name_input.clear()
        self._schedule_section.clear()
        self._website_section.clear()
        self._apps_section.clear()
