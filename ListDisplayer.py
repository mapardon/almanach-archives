import lists_ops as tools
from ClickableIcon import ClickableIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


sunny_title_style = "\
            font: 35pt Mistral;\
            color: rgb(0, 61, 153);\
            "

sunny_vocabulary_style = "QLabel {\
                    font: 20pt GeosansLight;\
                    color: rgb(0, 61, 153);\
                   }"

sunny_win_style = "ListDisplayer {\
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\
                        stop:0 white,\
                        stop:1 rgb(102, 163, 255));\
            background-position: center;\
        }"

dusk_title_style = "\
            font: 35pt Mistral;\
            color: rgb(0, 61, 153);\
            "

dusk_vocabulary_style = "QLabel {\
                    font: 20pt GeosansLight;\
                    color: rgb(255, 255, 255);\
                   }"

dusk_win_style = "ListDisplayer {\
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\
                        stop:0 rgb(0, 26, 102),\
                        stop:1 rgb(250, 120, 7));\
            background-position: center;\
        }"


class ListDisplayer(QMainWindow):
    def __init__(self, listname, dusk):
        # window inits
        super(ListDisplayer, self).__init__()
        self.resize(600, 800)
        self.setWindowTitle("ListDisplayer")

        # define styles
        if dusk:
            styles = {"win": dusk_win_style, "title": dusk_title_style, "voc": dusk_vocabulary_style}
        else:
            styles = {"win": sunny_win_style, "title": sunny_title_style, "voc": sunny_vocabulary_style}
        self.setStyleSheet(styles["win"])

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # title
        self.title = QLabel("Encore des mots ...", self.centralWidget)
        self.title.setStyleSheet(styles["title"])
        self.title_lt = QHBoxLayout()
        self.title_lt.addStretch()
        self.title_lt.addWidget(self.title)
        self.title_lt.addStretch()

        # words management & display {{{

        # load words and compose bunches
        self.words, self.trads, self.nb_pages = tools.list_chopper(listname)
        self.cur_page = int()

        self.cur_words = QLabel(self.words[0], self.centralWidget)
        self.cur_trads = QLabel(self.trads[0], self.centralWidget)
        self.cur_words.setStyleSheet(styles["voc"])
        self.cur_trads.setStyleSheet(styles["voc"])
        # }}}

        # Arrows {{{
        l_ar_ico = dusk and "Icons\\og_left_arrow.png" or "Icons\\left_arrow.png"
        r_ar_ico = dusk and "Icons\\og_right_arrow.png" or "Icons\\right_arrow.png"
        self.l_ar = ClickableIcon(QPixmap(l_ar_ico))
        self.r_ar = ClickableIcon(QPixmap(r_ar_ico))

        self.l_arr_lt = QVBoxLayout()
        self.l_arr_lt.addStretch()
        self.l_arr_lt.addWidget(self.l_ar)
        self.r_arr_lt = QVBoxLayout()
        self.r_arr_lt.addStretch()
        self.r_arr_lt.addWidget(self.r_ar)

        # make moving a real thing
        self.r_ar.clicked.connect(lambda: self.switch_page(True))
        self.l_ar.clicked.connect(lambda: self.switch_page(False))
        # }}}

        # words
        self.words_lt = QHBoxLayout()
        self.words_lt.addWidget(self.cur_words)
        self.words_lt.addStretch()
        self.words_lt.addWidget(self.cur_trads)
        self.words_lt.addStretch()

        # words n title
        self.words_n_title_lt = QVBoxLayout()
        self.words_n_title_lt.addLayout(self.title_lt)
        self.words_n_title_lt.addStretch()
        self.words_n_title_lt.addLayout(self.words_lt)
        self.words_n_title_lt.addStretch()


        # layout
        self.lt = QHBoxLayout(self.centralWidget)
        self.lt.addLayout(self.l_arr_lt)
        self.lt.addStretch()
        self.lt.addLayout(self.words_n_title_lt)
        self.lt.addStretch()
        self.lt.addLayout(self.r_arr_lt)

    def switch_page(self, right_ar):
        if right_ar:
            self.cur_page = (self.cur_page + 1)%self.nb_pages
        else:
            self.cur_page = (self.cur_page - 1)%self.nb_pages
        self.cur_words.setText(self.words[self.cur_page])
        self.cur_trads.setText(self.trads[self.cur_page])
