#! /usr/bin/python3

import sys

from PySide2 import QtWidgets

from MainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    #Initialise and set size of main_window
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.setMinimumSize(640, 480)
    main_window.show()
    version = "0.2.2"

    sys.exit(app.exec_())
