# coding: utf8
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QWidget


class PushButtonWithItem(QPushButton):

    clicked_with_item = Signal(object)

    def __init__(self, item: object, title: str = "", parent: QWidget = None):
        super().__init__(title, parent)
        self.item = item
        self.clicked.connect(self.on_self_clicked)

    def on_self_clicked(self):
        self.clicked_with_item.emit(self.item)
