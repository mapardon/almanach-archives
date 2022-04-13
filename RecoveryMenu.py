import os
import files_ops as tools

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from WindowUtils import WindowUtils
from messages import LIST_FOUND


class RecoveryMenu(WindowUtils):
    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        super(RecoveryMenu, self).__init__(wrap)

        self.other_lists = wrap.living_lists

        # Title {{{
        title = QLabel("Recovery")
        title.setFont(QFont('Courier', 12))

        # lay out
        title_layout = self.horizontal_menu_widget_layouter(title)
        # }}}

        # list selection {{{
        self.choose_list = wrap.dead_lists
        self.choose_list.setMinimumWidth(250)
        for filename in os.listdir(tools.TRASH):
            if filename.split('.')[1] == "dat":
                self.choose_list.addItem(filename.split('.')[0])
        # laying out
        choose_list_layout = self.horizontal_menu_widget_layouter(self.choose_list)
        # }}}

        # Recover list btn {{{
        recover_btn = QPushButton("Récupérer")
        recover_btn.setMinimumWidth(250)

        # layout
        recover_btn_layout = self.horizontal_menu_widget_layouter(recover_btn)

        # connect
        recover_btn.clicked.connect(lambda: self.launch_recovery())
        # }}}

        # Exit recovery mode
        prev_button = QPushButton("Retour", centralWidget)
        prev_button.setMinimumWidth(250)

        # laying out
        prev_button_layout = self.horizontal_menu_widget_layouter(prev_button)

        # connecting
        prev_button.clicked.connect(lambda i=0: baseStack.setCurrentIndex(i))
        # }}}

        # GROUPBOXING {{{
        gb_revive_lists = self.groupboxer("Resurrection", choose_list_layout, recover_btn_layout)
        # }}}

        # finalize : layout
        recovery_layout = QVBoxLayout()
        recovery_layout.addStretch()
        recovery_layout.addLayout(title_layout)
        recovery_layout.addStretch()
        recovery_layout.addLayout(gb_revive_lists)
        recovery_layout.addLayout(prev_button_layout)
        recovery_layout.addStretch()

        ownStack.setLayout(recovery_layout)

    def launch_recovery(self):
        filename = self.choose_list.currentText()
        fname_edited = "Récupérer la liste : {} ?".format(filename)

        if tools.is_homonym(filename, self.itemizator(self.other_lists)):
            self.informative_popup("Warning", LIST_FOUND)
        elif filename and self.interrogative_popup("Confirmation", fname_edited, ("Oui", "Non")):
            # make sure min 1 list exists (either nothing can be selected) and asking confirmation
            tools.resurrect(filename)
            self.choose_list.removeItem(self.choose_list.currentIndex())

            # update living lists
            self.wrap.living_lists.addItem(filename)