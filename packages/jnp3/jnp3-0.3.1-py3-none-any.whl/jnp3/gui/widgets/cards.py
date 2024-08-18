# coding: utf8
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QScrollArea
)
from .lines import HorizontalLine
from .buttons import PushButtonWithItem


class Card(QGroupBox):

    def __init__(self, title: str = "", icon: QIcon = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.icon = icon

        self.vly_m = QVBoxLayout()
        self.setLayout(self.vly_m)
        self.hly_top = QHBoxLayout()
        self.vly_m.addLayout(self.hly_top)

        self.lb_icon = QLabel(self)
        self.lb_title = QLabel(self.title, self)
        self.pbn_close = PushButtonWithItem(self, "❌", self)
        self.pbn_close.setFixedWidth(25)
        self.pbn_close.setFlat(True)
        self.hly_top.addWidget(self.lb_icon)
        self.hly_top.addWidget(self.lb_title)
        self.hly_top.addStretch(1)
        self.hly_top.addWidget(self.pbn_close)

        self.hln_1 = HorizontalLine(self)
        self.vly_m.addWidget(self.hln_1)

        self.cw = QLabel("Nothing here...", self)
        self.vly_m.addWidget(self.cw)

        if self.icon is not None:
            self.set_icon(self.icon)

    def set_central_widget(self, widget: QWidget):
        self.vly_m.removeWidget(self.cw)
        self.cw.deleteLater()

        self.cw = widget
        self.vly_m.addWidget(self.cw)

    def set_title(self, title: str):
        self.title = title
        self.lb_title.setText(title)

    def set_icon(self, icon: QIcon):
        self.icon = icon
        self.lb_icon.setText("")
        self.lb_icon.setPixmap(icon.pixmap(20, 20))


class CardsArea(QScrollArea):

    card_removed = Signal(Card)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.vly_m = QVBoxLayout()
        self.setLayout(self.vly_m)

        self.cw = QWidget(self)
        self.setWidget(self.cw)

        self.vly_cw = QVBoxLayout(self.cw)
        self.cw.setLayout(self.vly_cw)
        self.vly_cw.addStretch(1)

        self.cards: list[Card] = []

    def add_card(self, widget: QWidget = None, title: str = "", icon: QIcon = None) -> Card:
        card = Card(title, icon, parent=self)
        if widget is not None:
            card.set_central_widget(widget)
        card.pbn_close.clicked_with_item.connect(self.remove_card)
        self.vly_cw.insertWidget(self.vly_cw.count() - 1, card)
        self.cards.append(card)
        return card

    def remove_card(self, card: Card):
        self.vly_cw.removeWidget(card)
        self.cards.remove(card)
        card.deleteLater()

        self.card_removed.emit(card)
