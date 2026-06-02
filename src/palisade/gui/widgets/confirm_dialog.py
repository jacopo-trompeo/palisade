from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from palisade.gui.widgets.secondary_button import SecondaryButton


class ConfirmDialog(QDialog):
    def __init__(
        self,
        parent: QWidget | None,
        title: str,
        prompt_html: str,
        expected_word: str,
        confirm_label: str,
        confirm_kind: Literal["danger"] | Literal["primary"] = "danger",
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(440)
        self._expected = expected_word.strip().lower()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(14)

        prompt = QLabel(prompt_html)
        prompt.setWordWrap(True)
        prompt.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(prompt)

        self._input = QLineEdit()
        self._input.setPlaceholderText(expected_word)
        self._input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self._input)

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch(1)

        cancel_button = SecondaryButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        row.addWidget(cancel_button)

        self._confirm_btn = QPushButton(confirm_label)
        self._confirm_btn.setObjectName(
            "DangerButton" if confirm_kind == "danger" else "PrimaryButton"
        )
        self._confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._confirm_btn.setEnabled(False)
        self._confirm_btn.clicked.connect(self.accept)
        row.addWidget(self._confirm_btn)

        layout.addLayout(row)

    def _on_text_changed(self, text: str) -> None:
        self._confirm_btn.setEnabled(text.strip() == self._expected)


def confirm_delete(parent: QWidget | None, filter_name: str) -> bool:
    dlg = ConfirmDialog(
        parent,
        title="Delete filter",
        prompt_html=(
            f"To confirm deletion of filter <b>{filter_name}</b>, "
            "type <b>DELETE</b> in the box below."
        ),
        expected_word="DELETE",
        confirm_label="Confirm Delete",
        confirm_kind="danger",
    )

    return dlg.exec() == QDialog.DialogCode.Accepted


def confirm_disable(parent: QWidget | None, filter_name: str) -> bool:
    dlg = ConfirmDialog(
        parent,
        title="Disable filter",
        prompt_html=(
            f"To confirm disabling filter <b>{filter_name}</b>, "
            "type <b>DISABLE</b> in the box below."
        ),
        expected_word="DISABLE",
        confirm_label="Confirm Disable",
        confirm_kind="danger",
    )

    return dlg.exec() == QDialog.DialogCode.Accepted
