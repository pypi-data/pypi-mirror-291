# coding: utf8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtWidgets import (
    QWidget, QMessageBox
)
from PySide6.QtSvg import QSvgRenderer


def accept_warning(widget: QWidget, condition: bool,
                   caption: str = "Warning", text: str = "Are you sure to continue?") -> bool:
    if condition:
        b = QMessageBox.question(widget, caption, text)
        if b == QMessageBox.StandardButton.No:
            return True
    return False


def get_icon_from_svg(svg_data: str, w: int = None, h: int = None) -> QIcon:
    w = 128 if w is None else w
    h = 128 if h is None else h

    renderer = QSvgRenderer(svg_data.encode("utf-8"))
    pixmap = QPixmap(w, h)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)
