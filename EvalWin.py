import lists_ops as tools
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class EvalWin(QMainWindow):
    def __init__(self, mode=True, nb_q=5, cur_list=str()):
        super(EvalWin, self).__init__()
        self.setWindowTitle("Évaluation")
        self.setMinimumSize(350, 450)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # managing
        self.finished = bool()
        # on utilise une sorte de dictionnaire (comme sur disque) pour avoir question/solution/valeur à update
        # /!\ l'ordre peut être inversé : {question : réponse}, pas forcément {fr : en}
        self.test_sheet = tools.generate_quiz(nb_q, mode, cur_list)

        # Title {{{
        title = QLabel("Interrogation")
        title.setFont(QFont('Courier', 12))
        title_lt = self.horizontal_menu_widget_layouter(title)
        # }}}

        # questions, answers & solutions {{{
        self.test_sheet_wid = list()
        self.test_sheet_wid_lt = list()
        for q in self.test_sheet:
            new_lbl = QLabel(q)
            new_lin = QLineEdit()
            new_lin.setMaximumWidth(150)
            new_sol = QLabel(str())
            self.test_sheet_wid.append([new_lbl, new_lin, new_sol])

        # lt
        sub_vertical_lt = QVBoxLayout()
        for wid_lst in self.test_sheet_wid:
            tmp = QHBoxLayout()
            tmp.addWidget(wid_lst[0])
            tmp.addWidget(wid_lst[1])
            tmp.addWidget(wid_lst[2])
            sub_vertical_lt.addLayout(tmp)
        sub_vertical_lt.setAlignment(Qt.AlignRight)
        # }}}

        # correction btn {{{
        correction_btn = QPushButton("Correction")
        correction_btn.clicked.connect(lambda: self.launch_correction(mode, cur_list))
        correction_btn_lt = self.horizontal_menu_widget_layouter(correction_btn)
        # }}}

        # exit btn {{{
        exit_btn = QPushButton("Quitter")
        exit_btn.clicked.connect(lambda: self.exiter())
        exit_btn_lt = self.horizontal_menu_widget_layouter(exit_btn)
        # }}}

        # laying out
        self.baselayout = QVBoxLayout(self.centralWidget)
        lt = self.baselayout
        lt.addStretch()
        lt.addLayout(title_lt)
        lt.addStretch()
        # sublayout
        lt.addLayout(sub_vertical_lt)
        lt.addStretch()
        lt.addLayout(correction_btn_lt)
        lt.addLayout(exit_btn_lt)
        lt.addStretch()

    def launch_correction(self, mode, cur_listname):
        # update finished sentinel
        corrigeable = bool()
        if not self.finished:
            corrigeable = True
            for ans in self.test_sheet_wid:
                corrigeable &= bool(ans[1].text())

        if corrigeable:
            # display solution and save scores
            for ln, dt in zip(self.test_sheet_wid, self.test_sheet):
                # ln[0]:énoncé(label), ln[1]:user ans, ln[2]:sol_to_disp(label)
                # dt:key(énoncé), test_sheet[dt][0]:sol, test_sheet[dt][1]:updt_score
                ref = ln[2]
                sol = self.test_sheet[dt][0]
                ref.setText(sol)
                if self.correction(ln[1].text(), sol):
                    ref.setStyleSheet("color: rgb(98, 238, 0);")
                    self.test_sheet[dt][1] = 1
                else:
                    ref.setStyleSheet("color: rgb(249, 97, 17);")
                    self.test_sheet[dt][1] = -1

            tools.update_scores(self.test_sheet, mode, cur_listname)
            self.finished = True

        elif not self.finished:
            self.informative_popup("Avertissement", "Veuillez achever le test avant d'afficher la correction.")

    def exiter(self):
        if self.finished:
            self.close()
        else:
            self.informative_popup("Abandonner c pr les faibles", "Veuillez achever le test avant de quitter.")

    @staticmethod
    def horizontal_menu_widget_layouter(*wids):
        layout = QHBoxLayout()
        layout.addStretch()
        for w in wids:
            layout.addWidget(w)
        layout.addStretch()
        return layout

    @staticmethod
    def informative_popup(title, msg, btnname=str()):
        sentinel = QMessageBox()
        sentinel.setWindowTitle(title)
        sentinel.setText(msg)
        sentinel.setIcon(QMessageBox.Information)
        sentinel.setStandardButtons(sentinel.Ok)
        unique_button = sentinel.button(QMessageBox.Ok)
        if len(btnname):
            unique_button.setText(btnname)
        sentinel.exec_()

    @staticmethod
    def correction(ans, sol):
        same  = tools.serialize_entry(ans) == tools.serialize_entry(sol)
        s_ans = {tools.serialize_entry(s) for s in ans.split(",")}
        s_sol = {tools.serialize_entry(s) for s in sol.split(",")}
        return same or s_ans&s_sol
