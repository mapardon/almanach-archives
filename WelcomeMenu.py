import os
import lists_ops as tools

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from WindowUtils import WindowUtils
from ClickableIcon import ClickableIcon
from TalkWin import TalkWin
from messages import NO_LIST_FOUND, CONSEILS, BONNES_PRATIQUES, MAN_PAGES, LICENSE, EXP_ERR


class WelcomeMenu(WindowUtils):
    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        super(WelcomeMenu, self).__init__(wrap)
        self._baseStack = baseStack

        # mo' wins
        self.stop = TalkWin("Avertissement et usages", "Avertissement et usages", CONSEILS)
        self.pizza = TalkWin("Nommage des listes", "Nommage des listes", BONNES_PRATIQUES)
        self.ordi = TalkWin("Autres fonctionnalités", "Autres fonctionnalités", MAN_PAGES)
        self.sans = TalkWin("LiSans", "Droits d'auteur", LICENSE)

        # title {{{
        _title = QLabel("Almanach")
        _title.setFont(QFont('Courier', 18))

        # laying out
        title_layout = self.horizontal_menu_widget_layouter(_title)
        # }}}

        # list selection {{{

        #   ^
        #  /|\ ---> SHARED PARAMETER
        # /_•_\
        self.choose_list = wrap.living_lists

        self.choose_list.setMinimumWidth(250)
        for filename in os.listdir(tools.REPERTOIRE):
            if filename.split('.')[1] == "dat":
                self.choose_list.addItem(filename.split('.')[0])
        # laying out
        choose_list_layout = self.horizontal_menu_widget_layouter(self.choose_list)
        # }}}

        # delete list {{{
        del_list_button = QPushButton("Suppression", centralWidget)
        del_list_button.setMinimumWidth(250)

        # laying out
        del_list_button_layout = self.horizontal_menu_widget_layouter(del_list_button)

        # connecting
        del_list_button.clicked.connect(lambda: self.delete_list(wrap))
        # }}}

        # IMPORT - EXPORT {{{
        self.import_btn = QPushButton("Importer", centralWidget)
        self.export_btn = QPushButton("Exporter", centralWidget)
        self.import_btn.setMinimumWidth(120)
        self.export_btn.setMinimumWidth(120)

        # lt
        self.imp_exp_lt = self.horizontal_menu_widget_layouter(self.import_btn, self.export_btn)

        # konnekt
        self.import_btn.clicked.connect(self.importer)
        self.export_btn.clicked.connect(self.exporter)
        # }}}

        # /!\ RMQ /!\
        # Certains attributs sont utilisés, dans des méthodes, comme passés en paramètres
        # ET (au sein de la même fonction) comme référence (self.)

        # new list name (+ label) {{{
        new_list_label, self.new_list_namer = self.label_and_input("Intitulé", centralWidget, True)

        # laying out
        new_list_name_layout = self.horizontal_menu_widget_layouter(new_list_label, self.new_list_namer)
        # }}}

        # create new list & rename {{{
        rename_button = QPushButton("Renommer")
        rename_button.setMinimumWidth(250)

        new_list_button = QPushButton("Nouvelle liste", centralWidget)
        new_list_button.setMinimumWidth(250)

        # laying out
        new_list_button_layout = self.horizontal_menu_widget_layouter(new_list_button)
        rename_button_layout = self.horizontal_menu_widget_layouter(rename_button)

        # connecting
        new_list_button.clicked.connect(lambda: self.create_list(self.new_list_namer.text()))
        rename_button.clicked.connect(
            lambda: self.rename_list(self.choose_list.currentText(), self.new_list_namer.text()))
        # }}}

        # launch edit mode {{{
        launch_edit_mode_button = QPushButton("Édition", centralWidget)
        launch_edit_mode_button.setMinimumWidth(250)

        # laying out
        launch_edit_mode_button_layout = self.horizontal_menu_widget_layouter(launch_edit_mode_button)

        # connecting
        launch_edit_mode_button.clicked.connect(lambda: self.switch_menu(baseStack, 1))
        # }}}

        # launch evaluation mode {{{
        launch_eval_mode_button = QPushButton("Étude", centralWidget)
        launch_eval_mode_button.setMinimumWidth(250)

        # laying out
        launch_eval_mode_button_layout = self.horizontal_menu_widget_layouter(launch_eval_mode_button)

        # connecting
        launch_eval_mode_button.clicked.connect(lambda: self.switch_menu(baseStack, 2))
        # }}}

        # exit {{{
        exit_button = QPushButton("Quitter", centralWidget)
        exit_button.setMinimumWidth(250)
        exit_button.clicked.connect(self.exiter)

        # laying out
        exit_button_layout = self.horizontal_menu_widget_layouter(exit_button)

        # connecting
        exit_button.clicked.connect(self.exiter)
        # }}}

        # icons {{{
        stop_icon = ClickableIcon(QPixmap("Icons\\stop.png"))
        pizza_icon = ClickableIcon(QPixmap("Icons\\pizza.png"))
        ordi_icon = ClickableIcon(QPixmap("Icons\\ordi.png"))
        sans_icon = ClickableIcon(QPixmap("Icons\\sans.png"))

        # connecting
        stop_icon.clicked.connect(lambda: self.stop_ui())
        pizza_icon.clicked.connect(lambda: self.pizza_ui())
        ordi_icon.clicked.connect(lambda: self.ordi_ui())
        sans_icon.clicked.connect(lambda: self.sans_ui())

        # laying out
        icons_layout = QHBoxLayout()
        icons_layout.addStretch()
        icons_layout.addWidget(stop_icon)
        icons_layout.addWidget(pizza_icon)
        icons_layout.addWidget(ordi_icon)
        icons_layout.addWidget(sans_icon)
        # }}}

        # groupboxes
        # list selection
        layouted_gb1 = self.groupboxer("Gestion des listes", choose_list_layout, del_list_button_layout,
                                       self.imp_exp_lt)

        # lists management
        layouted_gb2 = self.groupboxer("Édition des listes", new_list_name_layout, new_list_button_layout,
                                       rename_button_layout)

        # mode selection
        layouted_gb3 = self.groupboxer("Activité", launch_edit_mode_button_layout, launch_eval_mode_button_layout,
                                       exit_button_layout)

        # finalize (layout the boxes)
        welcome_layout = QVBoxLayout()
        welcome_layout.addStretch()
        welcome_layout.addLayout(title_layout)
        welcome_layout.addStretch()
        welcome_layout.addLayout(layouted_gb1)
        welcome_layout.addLayout(layouted_gb2)
        welcome_layout.addLayout(layouted_gb3)
        welcome_layout.addStretch()
        welcome_layout.addLayout(icons_layout)

        ownStack.setLayout(welcome_layout)

    def delete_list(self, wrap):
        filename = self.choose_list.currentText()
        confirm_msg = "Supprimer la liste : {} ?".format(filename)
        homonym_msg = "Une liste {} existe déjà dans la poubelle.\nRenommez-la pour la supprimer.".format(filename)

        if filename and self.interrogative_popup("Confirmation", confirm_msg, ("Oui", "Non")):
            # make sure min 1 list exists (either nothing can be selected) and asking confirmation

            if filename in self.itemizator(wrap.dead_lists):
                self.informative_popup("Avertissement", homonym_msg)

            else:
                res = tools.delete_file(filename)

                if res == -1:
                    self.informative_popup("Avertissement", "Une erreur est survenue lors de la suppression.")

                else:
                    # update lists
                    self.choose_list.removeItem(self.choose_list.currentIndex())
                    wrap.dead_lists.addItem(filename)

    def create_list(self, filename):
        if self.easter_eggs_manager(filename):
            if filename == "__REC0VER__":
                self.switch_menu(self._baseStack, 3)
            elif not tools.is_regular_filename(filename) or tools.is_homonym(filename, self.itemizator(self.choose_list)):
                self.informative_popup("Avertissement",
                                       "Le nom renseigné devrait respecter les bonnes pratiques de nommage (pizza).")
            else:
                tools.create_file(filename)
                self.choose_list.addItem(filename)
                self.choose_list.setCurrentIndex(len(self.itemizator(self.choose_list)) - 1)
        self.new_list_namer.setText(str())

    def rename_list(self, old, new):
        if not tools.is_regular_filename(new) or new in self.itemizator(self.choose_list):
            self.informative_popup("Avertissement",
                                   "Le nom renseigné devrait respecter les bonnes pratiques de nommage (pizza).")

        elif new != "__REC0VER__" and new != "__S4LTY__":
            tools.rename(old, new)
            i = self.choose_list.currentIndex()
            self.choose_list.removeItem(i)
            self.choose_list.addItem(new)
            self.choose_list.setCurrentIndex(len(self.itemizator(self.choose_list)) - 1)
        self.new_list_namer.setText(str())

    def switch_menu(self, stack, index):
        cur_list = self.choose_list.currentText()
        if not cur_list and index < 3:
            self.informative_popup("Avertissement", NO_LIST_FOUND, "Je vais le faire !")
        elif index == 2 and tools.is_empty(self.choose_list.currentText()):
            self.informative_popup("Avertissement", "Votre liste est actuellement vide.")
        else:
            self.wrap.update_list(cur_list)
            stack.setCurrentIndex(index)

    def importer(self):
        """ask user to select file"""
        # fetch name & path
        desktop = os.path.expanduser("~/Desktop")
        filepath = QFileDialog.getOpenFileName(self, 'OpenFile', desktop, "Text files (*.txt)")[0]
        if not (filepath and self.interrogative_popup("Import", "Voulez-vous exporter la liste {} sur votre bureau ?".format(filepath))):
            return
        filename = filepath.split('/')[-1].split('.')[0]

        # check if can be imported
        if filename in self.itemizator(self.choose_list) or not tools.is_regular_filename(filename):
            self.informative_popup("Avertissement",
                        "Le nom de la liste à importer existe déjà dans le répertoire.")

        elif tools.file_import(filepath, filename) == -1:
            self.informative_popup("Avertissement",
                        "Une erreur est survenue lors de l'import de la liste. Assurez-vous que le "+\
                        "fichier importé respecte le schéma utilisé par l'application (ordi).")

        else:
            # ajouter ce nom à la liste
            self.choose_list.addItem(filename)

    def exporter(self):
        cur_lname = self.choose_list.currentText()
        conf = self.interrogative_popup("Import",
                        "Voulez-vous exporter la liste {} sur votre bureau ?".format(self.choose_list.currentText()))
        if conf:
            exc = tools.file_export(cur_lname)
            if exc == -2:
                self.informative_popup("Erreur", EXP_ERR.format(cur_lname))
            elif exc == -1:
                self.informative_popup("Erreur", "Une erreur est survenue lors de l'externalisation de votre liste.")

    def stop_ui(self):
        if self.stop.isHidden() and self.pizza.isHidden() and self.ordi.isHidden() and self.sans.isHidden():
            self.stop.show()

    def pizza_ui(self):
        if self.stop.isHidden() and self.pizza.isHidden() and self.ordi.isHidden() and self.sans.isHidden():
            self.pizza.show()

    def ordi_ui(self):
        if self.stop.isHidden() and self.pizza.isHidden() and self.ordi.isHidden() and self.sans.isHidden():
            self.ordi.show()

    def sans_ui(self):
        if self.stop.isHidden() and self.pizza.isHidden() and self.ordi.isHidden() and self.sans.isHidden():
            self.sans.show()
