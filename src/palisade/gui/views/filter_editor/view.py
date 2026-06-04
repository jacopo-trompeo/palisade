from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from palisade import ipc
from palisade.db.database import create_filter, get_filter, update_filter
from palisade.db.models import Filter, ScheduleType
from palisade.dbi import get_edit_lock_seconds
from palisade.gui.views.filter_editor.action_section import ActionSection
from palisade.gui.views.filter_editor.apps_section import AppsSection
from palisade.gui.views.filter_editor.schedule_section import ScheduleSection
from palisade.gui.views.filter_editor.websites_section import WebsitesSection
from palisade.gui.widgets.section_title import SectionTitle


class _EditLockBanner(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("EditLockBanner")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        self._label = QLabel("Fields unlock in ...")
        self._label.setObjectName("EditLockLabel")
        layout.addWidget(self._label)

        self._bar = QProgressBar()
        self._bar.setObjectName("EditLockBar")
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(6)
        layout.addWidget(self._bar)

    def configure(self, total: int) -> None:
        self._bar.setRange(0, total)
        self._bar.setValue(0)

    def update_progress(self, elapsed: int, remaining: int) -> None:
        self._bar.setValue(elapsed)
        self._label.setText(f"Fields unlock in {remaining}s")


class FilterEditorView(QWidget):
    save_requested = Signal()

    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window
        self._editing_id: str | None = None
        self._edit_lock_timer: QTimer | None = None
        self._edit_lock_remaining = 0
        self._edit_lock_total = 0
        self._lockable_widgets: list[QWidget] = []

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

        self._lock_banner = _EditLockBanner()
        self._lock_banner.setVisible(False)
        layout.addWidget(self._lock_banner)

        layout.addWidget(SectionTitle("Name"))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Filter name...")
        self._name_input.setObjectName("FilterInput")
        self._lockable_widgets.append(self._name_input)
        layout.addWidget(self._name_input)

        layout.addWidget(SectionTitle("Schedule"))
        self._schedule = ScheduleSection()
        self._lockable_widgets.append(self._schedule)
        layout.addWidget(self._schedule)

        layout.addWidget(SectionTitle("Blocked Websites"))
        self._websites = WebsitesSection()
        self._lockable_widgets.append(self._websites)
        layout.addWidget(self._websites)

        layout.addWidget(SectionTitle("Blocked apps"))
        self._apps = AppsSection()
        self._lockable_widgets.append(self._apps)
        layout.addWidget(self._apps)

        layout.addSpacing(8)

        actions = ActionSection()
        actions.cancel_requested.connect(self._on_cancel)
        actions.save_requested.connect(self._on_save)
        layout.addWidget(actions)

        layout.addStretch(1)

    def load(self, filter_id: str | None) -> None:
        self._editing_id = filter_id
        self._stop_edit_lock()

        if filter_id is None:
            self._title_label.setText("Add Filter")
            self._set_value(Filter())
            self._set_inputs_enabled(True)
            self._lock_banner.setVisible(False)
            return

        flt = get_filter(filter_id)
        if flt is None:
            self._main_window.navigate("home")
            return
        self._title_label.setText("Edit Filter")
        self._set_value(flt)
        self._set_inputs_enabled(False)
        self._lock_banner.setVisible(True)
        self._start_edit_lock()

    def _start_edit_lock(self) -> None:
        self._edit_lock_total = get_edit_lock_seconds()
        self._edit_lock_remaining = self._edit_lock_total
        self._lock_banner.configure(self._edit_lock_total)
        self._lock_banner.update_progress(0, self._edit_lock_remaining)

        self._edit_lock_timer = QTimer(self)
        self._edit_lock_timer.setInterval(1000)
        self._edit_lock_timer.timeout.connect(self._tick_edit_lock)
        self._edit_lock_timer.start()

    def _tick_edit_lock(self) -> None:
        self._edit_lock_remaining -= 1
        elapsed = self._edit_lock_total - self._edit_lock_remaining
        self._lock_banner.update_progress(elapsed, self._edit_lock_remaining)
        if self._edit_lock_remaining <= 0:
            self._stop_edit_lock()
            self._set_inputs_enabled(True)
            self._lock_banner.setVisible(False)

    def _stop_edit_lock(self) -> None:
        if self._edit_lock_timer is not None:
            self._edit_lock_timer.stop()
            self._edit_lock_timer.deleteLater()
            self._edit_lock_timer = None

    def _set_inputs_enabled(self, enabled: bool) -> None:
        for w in self._lockable_widgets:
            w.setEnabled(enabled)

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

        ipc.notify({"type": "filters_changed"})
        self._main_window.navigate("home")
        self.save_requested.emit()
