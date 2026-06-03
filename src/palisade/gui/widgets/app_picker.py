import os
import shlex
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.widgets.primary_button import PrimaryButton
from palisade.gui.widgets.secondary_button import SecondaryButton

XDG_APP_DIRS = [
    Path.home() / ".local" / "share" / "applications",
    Path("/usr/share/applications"),
    Path("/usr/local/share/applications"),
    Path.home() / ".local" / "share" / "flatpak" / "exports" / "share" / "applications",
    Path("/var/lib/flatpak/exports/share/applications"),
]


@dataclass(frozen=True)
class DesktopApp:
    name: str
    exec_name: str
    icon: str
    source_path: str


def _exec_basename(exec_line: str) -> str:
    if not exec_line:
        return ""

    try:
        tokens = shlex.split(exec_line)
    except ValueError:
        tokens = exec_line.split()

    for t in tokens:
        if not t.startswith("%") and "=" not in t:
            return os.path.basename(t)

    return ""


def _parse_desktop_file(path: Path) -> DesktopApp | None:
    try:
        cp = ConfigParser(interpolation=None, strict=False)
        cp.optionxform = str  # type: ignore[assignment]
        cp.read(path, encoding="utf-8")
    except Exception:
        return None

    section = "Desktop Entry"
    if section not in cp:
        return None

    entry = cp[section]
    if entry.get("Type", "").strip() != "Application":
        return None

    if entry.get("NoDisplay", "").strip().lower() == "true":
        return None

    if entry.get("Hidden", "").strip().lower() == "true":
        return None

    name = entry.get("Name", "").strip()
    if not name:
        return None

    exec_name = _exec_basename(entry.get("Exec", "").strip())
    if not exec_name:
        exec_name = path.stem

    icon = entry.get("Icon", "").strip()
    return DesktopApp(name=name, exec_name=exec_name, icon=icon, source_path=str(path))


def _discover_installed_apps() -> list[DesktopApp]:
    seen: dict[str, DesktopApp] = {}

    for d in XDG_APP_DIRS:
        if not d.exists():
            continue
        try:
            for fp in sorted(d.glob("*.desktop")):
                app = _parse_desktop_file(fp)
                if app is None:
                    continue

                seen.setdefault(app.exec_name, app)
        except PermissionError:
            continue

    return sorted(seen.values(), key=lambda a: a.name.lower())


class _SearchInput(QLineEdit):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setPlaceholderText("Search...")


class _AppPickerList(QListWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName("AppPickerList")
        self.setIconSize(QSize(24, 24))
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)


class AppPickerDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("Browse installed apps")
        self.setModal(True)
        self.resize(520, 540)

        self._apps = _discover_installed_apps()
        self._picked: list[DesktopApp] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Select one or more apps to block:"))

        self._search = _SearchInput()
        self._search.textChanged.connect(self._filter_list)
        layout.addWidget(self._search)

        self._list = _AppPickerList()
        layout.addWidget(self._list, 1)

        self._populate(self._apps)

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch(1)

        cancel_button = SecondaryButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        row.addWidget(cancel_button)

        ok_button = PrimaryButton("Ok")
        ok_button.clicked.connect(self._on_accept)
        row.addWidget(ok_button)

        layout.addLayout(row)

    def _populate(self, apps: list[DesktopApp]) -> None:
        self._list.clear()

        for app in apps:
            item = QListWidgetItem(f"{app.name}  ·  {app.exec_name}")
            if app.icon:
                qi = QIcon.fromTheme(app.icon)
                if not qi.isNull():
                    item.setIcon(qi)

            item.setData(Qt.ItemDataRole.UserRole, app)
            self._list.addItem(item)

    def _filter_list(self, text: str) -> None:
        t = text.strip().lower()

        if not t:
            filtered = self._apps
        else:
            filtered = [
                a for a in self._apps if t in a.name.lower() or t in a.exec_name.lower()
            ]

        self._populate(filtered)

    def _on_accept(self) -> None:
        self._picked = [
            self._list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self._list.count())
            if self._list.item(i).isSelected()
        ]

        self.accept()

    @property
    def picked(self) -> list[DesktopApp]:
        return self._picked
