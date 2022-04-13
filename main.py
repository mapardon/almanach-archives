""" ====================================================================================
 *
 *       Filename:  main.py
 *        Project:  Almanach
 *
 *    Description:  Almanach (UI) boot
 *
 *        Version:  1.x
 *        Created:  July 2020
 *       Revision:  Himself
 *    Interpreter:  Python 3.8.5
 *
 *         Author:  Mathieu Pardon (Mathilde), mathieu.pardon.20@gmail.com
 *   Organization:  Mathieu Company Limited (c)
 *
 * =====================================================================================
 """

import sys
from WindowUI import WindowUI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFontDatabase


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_icon = QIcon("Icons\\main_book.png")
    app.setWindowIcon(app_icon)
    app.setStyle('Fusion')

    QFontDatabase.addApplicationFont("Fonts\\Mistral.ttf")
    QFontDatabase.addApplicationFont("Fonts\\GeosansLight.ttf")

    ui = WindowUI()
    ui.show()
    sys.exit(app.exec_())
