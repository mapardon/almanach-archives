import lists_ops as tools

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from WindowUtils import WindowUtils
from messages import UNSUCCESSFUL_SEARCH


class EditMenu(WindowUtils):
    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        super(EditMenu, self).__init__(wrap)

        # title {{{
        title = QLabel("Édition")
        title.setFont(QFont('Courier', 12))

        # laying out
        title_layout = self.horizontal_menu_widget_layouter(title)
        # }}}

        # new entree {{{
        new_word_label, self.new_word_input = self.label_and_input("Terme", centralWidget)

        # laying out
        new_word_layout = self.horizontal_menu_widget_layouter(new_word_label, self.new_word_input)
        # }}}

        # new translation (+ label) {{{
        new_translation_label, self.new_translation_input = self.label_and_input("Traduction(s)", centralWidget)

        # laying out
        new_translation_layout = self.horizontal_menu_widget_layouter(new_translation_label, self.new_translation_input)
        # }}}

        # edition buttons (add new and modify) {{{
        insertion_button = QPushButton("Ajouter")
        insertion_button.setMinimumWidth(250)
        modify_button = QPushButton("Modifier")
        modify_button.setMinimumWidth(250)

        # laying out
        insertion_button_layout = self.horizontal_menu_widget_layouter(insertion_button)
        modify_button_layout = self.horizontal_menu_widget_layouter(modify_button)

        # connecting
        insertion_button.clicked.connect(lambda: self.new_entry())
        modify_button.clicked.connect(lambda: self.modify_entry())
        # }}}

        # lists management {{{
        management_label, self.management_input = self.label_and_input("Terme", centralWidget)

        # laying out
        # check -> groupboxing, gb_management

        # buttonz
        management_search = QPushButton("Recherche")
        management_search.setMinimumWidth(250)
        management_deletion = QPushButton("Suppression")
        management_deletion.setMinimumWidth(250)

        # layin' out
        management_search_layout = self.horizontal_menu_widget_layouter(management_search)
        management_deletion_layout = self.horizontal_menu_widget_layouter(management_deletion)

        # konnekt
        management_search.clicked.connect(lambda: self.search())
        management_deletion.clicked.connect(lambda: self.remove_entry())
        # }}}

        # random entry {{{
        random_btn = QPushButton("Sélection aléatoire")
        random_btn.setMinimumWidth(250)

        # layout : voir gb_other

        # konnekt
        random_btn.clicked.connect(lambda: self.random_entry())
        # }}}

        # previous {{{
        prev_button = QPushButton("Retour")
        prev_button.setMinimumWidth(250)

        # laying out
        prev_button_layout = self.horizontal_menu_widget_layouter(prev_button)

        # connecting
        prev_button.clicked.connect(lambda i=0: baseStack.setCurrentIndex(i))
        # }}}

        # groupboxing !
        # user inputs
        gb_new_entree = self.groupboxer("Insertion", new_word_layout, new_translation_layout, insertion_button_layout,
                                        modify_button_layout)

        gb_management = self.groupboxer("Gestion",
                                        self.horizontal_menu_widget_layouter(management_label, self.management_input),
                                        management_search_layout, management_deletion_layout)

        gb_other = self.groupboxer("Accessoires", self.horizontal_menu_widget_layouter(random_btn),
                                   prev_button_layout)

        # finalize (layout) {{{

        edit_layout = QVBoxLayout()
        edit_layout.addStretch()
        edit_layout.addLayout(title_layout)
        edit_layout.addStretch()
        edit_layout.addLayout(gb_new_entree)
        edit_layout.addLayout(gb_management)
        edit_layout.addLayout(gb_other)
        edit_layout.addStretch()

        ownStack.setLayout(edit_layout)
        # }}}

    def new_entry(self):
        """ Sorte de wrapper à la fonction d'insertion d'entrée pour effectuer
        les tests utiles (validation de l'entrée...) AINSI QUE la standardisation
        des entrées (et aussi, le cas échéant, la génération d'un popup) """

        w, t = tools.serialize_entry(self.new_word_input.text()), tools.serialize_entry(self.new_translation_input.text())
        check_search = tools.search_entry(self.wrap.get_cur_list(), w)

        # ajoutable
        if tools.is_regular_entry(w) and tools.is_regular_entry(t):
            ret = tools.add_entry(self.wrap.get_cur_list(), w, t)

            # existe déjà
            if ret == -2:
                self.informative_popup("Insertion",
                    "Cette entrée existe déjà dans la liste sélectionnée ({} : {}).".format(w[0].upper() + w[1:],
                                                                                check_search[0].upper() + check_search[1:]))
            elif ret == -1:
                self.informative_popup("Avertissement", "Une erreur est survenue lors de l'insertion.")
        # non ajoutable
        else:
            self.informative_popup("Insertion",
                "Tous les champs relatifs à l'insertion devraient être remplis.")

        self.new_word_input.setText(str())
        self.new_translation_input.setText(str())

    def modify_entry(self):
        w, n_t = tools.serialize_entry(self.new_word_input.text()), tools.serialize_entry(self.new_translation_input.text())
        check_search = tools.search_entry(self.wrap.get_cur_list(), w)
        if not check_search:
            self.informative_popup("Modification", "Cette entrée n'existe pas dans la liste sélectionnée.")
        else:
            tools.modify_entry(self.wrap.get_cur_list(), w, n_t)

        self.new_word_input.setText(str())
        self.new_translation_input.setText(str())

    def search(self):
        wanted, res = tools.serialize_entry(self.management_input.text()), str()
        res = tools.search_entry(self.wrap.get_cur_list(), wanted)

        if not res:
            self.informative_popup("Requête", UNSUCCESSFUL_SEARCH)
        else:
            self.informative_popup("Requête", "{1} : {0}".format(res[0].upper() + res[1:], wanted[0].upper() + wanted[1:]))
        self.management_input.setText(str())

    def remove_entry(self):
        target, res = tools.serialize_entry(self.management_input.text()), str()
        res = tools.search_entry(self.wrap.get_cur_list(), target)

        if not res:
            self.informative_popup("Suppression", UNSUCCESSFUL_SEARCH)
        elif self.interrogative_popup("Suppression", "Supprimer l'entrée : {} ?".format(target), ("Oui", "Non")):
            tools.del_entry(self.wrap.get_cur_list(), target)
        self.management_input.setText(str())

    def random_entry(self):
        modnar = tools.random_choice(self.wrap.get_cur_list())
        res = tools.search_entry(self.wrap.get_cur_list(), modnar)
        if not res:
            self.informative_popup("Probas&Stats", "Votre liste est actuellement vide.")
        else:
            self.informative_popup("Probas&Stats", "{} : {}".format(modnar[0].upper() + modnar[1:], res[0].upper() + res[1:]),
                               "Quitter")
