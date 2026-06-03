from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from palisade.db.database import create_filter, get_filter, update_filter
from palisade.db.models import Filter, ScheduleType
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
        self._editing_id: str | None = None

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
        self._schedule = ScheduleSection()
        layout.addWidget(self._schedule)

        layout.addWidget(SectionTitle("Blocked Websites"))
        self._websites = WebsitesSection()
        layout.addWidget(self._websites)

        layout.addWidget(SectionTitle("Blocked apps"))
        self._apps = AppsSection()
        layout.addWidget(self._apps)

        layout.addSpacing(8)

        actions = ActionSection()
        actions.cancel_requested.connect(self._on_cancel)
        actions.save_requested.connect(self._on_save)
        layout.addWidget(actions)

        layout.addStretch(1)

    def load(self, filter_id: str | None) -> None:
        self._editing_id = filter_id
        if filter_id is None:
            self._title_label.setText("Add Filter")
            self._set_value(Filter())
            return

        flt = get_filter(filter_id)
        if flt is None:
            self._main_window.navigate("home")
            return
        self._title_label.setText("Edit Filter")
        self._set_value(flt)

    def _set_value(self, flt: Filter) -> None:
        self._name_input.setText(flt.name)
        self._schedule.set_value(flt.schedule)
        self._websites.set_value(flt.blocked_websites)
        self._apps.set_value(flt.blocked_apps)

    def _on_cancel(self) -> None:
        self._main_window.navigate("home")

    def _on_save(self) -> None:
        name = self._name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Name required", "Please give the filter a name.")
            return

        schedule = self._schedule.value()
        if schedule.type == ScheduleType.CUSTOM:
            if not schedule.days:
                QMessageBox.warning(self, "No days selected", "Pick at least one day.")
                return
            if not schedule.time_ranges:
                QMessageBox.warning(
                    self, "No time range", "Add at least one time range."
                )
                return

        websites = self._websites.value()
        apps = self._apps.value()

        if self._editing_id is None:
            flt = Filter(
                name=name,
                schedule=schedule,
                blocked_websites=websites,
                blocked_apps=apps,
                enabled=True,
            )
            create_filter(flt)
        else:
            flt = get_filter(self._editing_id)
            if flt is None:
                self._main_window.navigate("home")
                return
            flt.name = name
            flt.schedule = schedule
            flt.blocked_websites = websites
            flt.blocked_apps = apps
            update_filter(flt)

        self._main_window.navigate("home")
        self.save_requested.emit()
