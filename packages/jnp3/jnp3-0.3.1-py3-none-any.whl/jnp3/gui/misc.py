# coding: utf8
from PySide6.QtWidgets import (
    QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtSql import QSqlDatabase


def accept_warning(widget: QWidget, condition: bool,
                   caption: str = "Warning", text: str = "Are you sure to continue?") -> bool:
    if condition:
        b = QMessageBox.question(widget, caption, text)
        if b == QMessageBox.StandardButton.No:
            return True
    return False


def get_sql_database(conn_name: str, file_path: str) -> QSqlDatabase:
    if QSqlDatabase.contains(conn_name):
        db = QSqlDatabase.database(conn_name, open=False)
    else:
        db = QSqlDatabase.addDatabase("QSQLITE", conn_name)
        db.setDatabaseName(file_path)

    return db


def change_color(widget: QWidget,
                 role: QPalette.ColorRole,
                 color: str | Qt.GlobalColor):
    pal = widget.palette()
    pal.setColor(role, color)
    widget.setPalette(pal)


def change_font(widget: QWidget, family: str, size: int, bold: bool = False):
    font = widget.font()
    font.setFamily(family)
    font.setPointSize(size)
    font.setBold(bold)
    widget.setFont(font)
