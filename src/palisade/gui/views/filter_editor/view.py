from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.views.filter_editor.action_section import ActionSection
from palisade.gui.views.filter_editor.apps_section import AppsSection
from palisade.gui.views.filter_editor.schedule_section import ScheduleSection
from palisade.gui.views.filter_editor.websites_section import WebsitesSection
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
        self._name_input.setObjectName("FilterInput")
        layout.addWidget(self._name_input)

        layout.addWidget(SectionTitle("Schedule"))
        layout.addWidget(ScheduleSection())

        layout.addWidget(SectionTitle("Blocked Websites"))
        layout.addWidget(WebsitesSection())

        layout.addWidget(SectionTitle("Blocked apps"))
        layout.addWidget(AppsSection())

        layout.addSpacing(8)

        layout.addWidget(ActionSection())

        layout.addStretch(1)
