from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TalkWin(QMainWindow):
    def __init__(self, header, title, msg):
        super(TalkWin, self).__init__()
        self.setWindowTitle(header)
        self.setMinimumHeight(950)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # title {{{
        _title = QLabel(title+'\n')
        f = QFont('Courier', 18)
        f.setItalic(True)
        _title.setFont(f)

        # laying out
        title_lt = self.horizontal_menu_widget_layouter(_title)
        # }}}

        # text (basically what this class is defined for) {{{
        talk = QLabel(msg)
        font = (title != header) and "Comic Sans MS" or "Courier"
        talk.setStyleSheet("font: 11pt " + font + ";\
        color: rgb(0, 62, 168 );\
        border-style: dot-dot-dash;\
        border-radius: 4px; border-width: 2px;\
        border-color: rgba(0,0,0,100);")

        talk_lt = self.horizontal_menu_widget_layouter(talk)
        talk_lt.setAlignment(Qt.AlignCenter)
        # }}}

        # finalize layouts
        self.baselayout = QVBoxLayout(self.centralWidget)
        lt = self.baselayout
        lt.addStretch()
        lt.addLayout(title_lt)
        lt.addStretch()
        lt.addLayout(talk_lt)
        lt.addStretch()


    @staticmethod
    def horizontal_menu_widget_layouter(*wids):
        layout = QHBoxLayout()
        layout.addStretch()
        for w in wids:
            layout.addWidget(w)
        layout.addStretch()
        return layout