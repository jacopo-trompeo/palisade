from PySide6.QtWidgets import QLayout, QWidget


def iter_layout_widgets[T: QWidget](
    layout: QLayout, of_type: type[T] = QWidget
) -> list[T]:
    widgets: list[T] = []
    for i in range(layout.count()):
        item = layout.itemAt(i)
        widget = item.widget() if item is not None else None
        if isinstance(widget, of_type):
            widgets.append(widget)
    return widgets


def clear_layout(layout: QLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item is None:
            continue
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
