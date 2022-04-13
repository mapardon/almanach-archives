from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ClickableIcon(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ClickableIcon, self).__init__(parent)
        self.pixmap = pixmap
        self.setMinimumSize(25, 25)
        self.setMaximumSize(60, 60)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()