import sys
import os
import setproctitle
from PySide2 import QtWidgets, QtGui
from CONSTANTS import get_resource

from MainWindow import MainWindow

if __name__ == "__main__":
    os.putenv("QT_QPA_PLATFORM", "xcb")
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Pepys")
    app.setApplicationDisplayName("Pepys")
    app.setWindowIcon(QtGui.QIcon(get_resource("icons/appicons/icon.svg")))
    setproctitle.setproctitle("Pepys")
    #Initialise and set size of main_window
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.setMinimumSize(640, 480)
    main_window.show()
    version = "0.3.0"

    sys.exit(app.exec_())
