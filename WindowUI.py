import files_ops as tools
from PyQt5.QtWidgets import *
from WelcomeMenu import WelcomeMenu
from EditMenu import EditMenu
from StudyMenu import StudyMenu
from RecoveryMenu import RecoveryMenu


class WindowUI(QMainWindow):
    def __init__(self):
        # window pars
        super(WindowUI, self).__init__()
        self.setMinimumSize(450, 600)
        self.setWindowTitle("Almanach")

        # current vocabulary list
        self.cur_list = str()

        # init repositories
        tools.init_util_dirs()

        # monthly trash cleaner
        tools.clear_trash()

        # central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # shared lists (defined here but used ("friendship", lol) and displayed elsewhere) {{
        self.living_lists = QComboBox(self.centralWidget)
        self.dead_lists = QComboBox(self.centralWidget)
        # }}

        # stacking
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        self.Stack = QStackedWidget(self)
        WelcomeMenu(self.centralWidget, self.Stack, self.stack1, self)
        EditMenu(self.centralWidget, self.Stack, self.stack2, self)
        StudyMenu(self.centralWidget, self.Stack, self.stack3, self)
        RecoveryMenu(self.centralWidget, self.Stack, self.stack4, self)

        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        # laying out
        self.baselayout = QVBoxLayout(self.centralWidget)
        self.baselayout.addWidget(self.Stack)

    def get_cur_list(self):
        return self.cur_list

    def update_list(self, new_cur_list):
        self.cur_list = new_cur_list
