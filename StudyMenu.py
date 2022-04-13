from WindowUtils import WindowUtils
from EvalWin import EvalWin
from ListDisplayer import ListDisplayer

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StudyMenu(WindowUtils):
    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        super(StudyMenu, self).__init__(wrap)

        # sub window revision
        self.reviz = None

        # sub window interrogation
        self.interro = None

        # title {{{
        title = QLabel("Étude", centralWidget)
        title.setFont(QFont('Courier', 12))

        # laying out
        title_layout = self.horizontal_menu_widget_layouter(title)
        # }}}

        # PARTIE REVISION {{{{{

        # select style {{{
        style_lb = QLabel("Style d'affichage")
        self.cur_style = True
        self.sunny_choice = QRadioButton("Sunny")
        self.dusk_choice = QRadioButton("Dusk")
        self.dusk_choice.setChecked(True)

        # update selection
        self.sunny_choice.toggled.connect(lambda: self.change_style())
        self.dusk_choice.toggled.connect(lambda: self.change_style())

        # layout
        style_label_layout = self.horizontal_menu_widget_layouter(style_lb)
        style_choice_lb_lt = self.horizontal_menu_widget_layouter(self.sunny_choice, self.dusk_choice)

        # }}}

        # display list {{{
        disp_list_btn = QPushButton("Révision", centralWidget)
        disp_list_btn.setMinimumWidth(250)

        # konnekt
        disp_list_btn.clicked.connect(lambda: self.launch_reviz())

        # layout
        gen_interro_btn_lt = self.horizontal_menu_widget_layouter(disp_list_btn)
        # }}}

        # GROUPBOXING
        reviz_gb = self.groupboxer("Révision", style_label_layout, style_choice_lb_lt,
                                   gen_interro_btn_lt)
        # }}}}} ENDOF REVISION

        # PARTIE EVALUATION {{{{{

        # mode selection {{{
        radio_label = QLabel("Réponses à fournir")
        self.original_mode = True
        self.radio_btn_og = QRadioButton("Langue originale", centralWidget)
        self.radio_btn_og.setChecked(True)
        self.radio_btn_oz = QRadioButton("Langue étudiée", centralWidget)

        # dè kennekt
        self.radio_btn_og.toggled.connect(lambda: self.switch_mode())
        self.radio_btn_oz.toggled.connect(lambda: self.switch_mode())

        # layin out
        radio_label_layout = self.horizontal_menu_widget_layouter(radio_label)
        radio_btn_1_layout = self.horizontal_menu_widget_layouter(self.radio_btn_og)
        radio_btn_2_layout = self.horizontal_menu_widget_layouter(self.radio_btn_oz)
        # }}}

        # number of questions {{{
        nb_q_lb = QLabel("Nombre de questions")
        self.visual_nb_q = QLabel("5")
        self.nb_q = QSlider(Qt.Horizontal, centralWidget)
        self.nb_q.setMinimum(5)
        self.nb_q.setMaximum(10)
        self.nb_q.setSingleStep(1)
        self.nb_q.setTickInterval(1)
        self.nb_q.setTickPosition(QSlider.TicksBelow)

        # konnekt
        self.nb_q.valueChanged.connect(lambda: self.visual_nb_q.setText(str(self.nb_q.value())))

        # layout
        nb_q_lb_lt = self.horizontal_menu_widget_layouter(nb_q_lb)
        nb_q_lt = self.horizontal_menu_widget_layouter(self.nb_q, self.visual_nb_q)
        # }}}

        # generate interro {{{
        gen_interro_btn = QPushButton("Interrogation", centralWidget)
        gen_interro_btn.setMinimumWidth(250)

        # konnekt
        gen_interro_btn.clicked.connect(lambda: self.launch_interro())

        # layout
        gen_interro_btn_lt = self.horizontal_menu_widget_layouter(gen_interro_btn)
        # }}}

        # groupboxing
        eval_gb = self.groupboxer("Étude", radio_label_layout, radio_btn_1_layout, radio_btn_2_layout,
                                     nb_q_lb_lt, nb_q_lt, gen_interro_btn_lt)

        # }}}}} ENDOF EVALUATION

        # goto prev menu {{{
        eval_prev_button = QPushButton("Retour", centralWidget)
        eval_prev_button.setMinimumWidth(250)

        # laying out
        eval_prev_button_layout = self.horizontal_menu_widget_layouter(eval_prev_button)

        # connecting
        eval_prev_button.clicked.connect(lambda: self.prev(baseStack))
        # }}}

        # finalize (layout) {{{
        eval_layout = QVBoxLayout()
        eval_layout.addStretch()
        eval_layout.addLayout(title_layout)
        eval_layout.addStretch()
        eval_layout.addLayout(reviz_gb)
        eval_layout.addLayout(eval_gb)
        eval_layout.addLayout(eval_prev_button_layout)
        eval_layout.addStretch()

        ownStack.setLayout(eval_layout)
        # }}}

    def change_style(self):
        if self.dusk_choice.isChecked():
            self.cur_style = True

        else:
            self.cur_style = False

    def switch_mode(self):
        if self.radio_btn_og.isChecked():
            self.original_mode = True

        else:
            self.original_mode = False

    def prev(self, baseStack):
        if (not self.interro or self.interro.isHidden()) and (not self.reviz or self.reviz.isHidden()):
            self.interro = None
            self.reviz = None
            baseStack.setCurrentIndex(0)

    def launch_reviz(self):
        if (not self.interro or self.interro.isHidden()) and (not self.reviz or self.reviz.isHidden()):
            self.reviz = ListDisplayer(self.wrap.get_cur_list(), self.cur_style)
            self.reviz.show()

    def launch_interro(self):
        if (not self.interro or self.interro.isHidden()) and (not self.reviz or self.reviz.isHidden()):
            self.interro = EvalWin(self.radio_btn_og.isChecked(), self.nb_q.value(), self.wrap.get_cur_list())
            self.interro.show()
