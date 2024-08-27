import sys
import os
from PySide6 import QtWidgets, QtCore

from node_editor import NodeEditor

if __name__ == '__main__':
    sys.dont_write_bytecode = True

    app = QtWidgets.QApplication(sys.argv)

    # file = QtCore.QFile('css:theme_dark.qss')
    # file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    # app.setStyleSheet(str(file.readAll(), 'utf-8'))

    my_main_window = NodeEditor()
    my_main_window.initUI()

    res = app.exec()
    sys.exit(res)
