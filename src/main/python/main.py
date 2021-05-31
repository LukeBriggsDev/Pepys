import os
import sys

import setproctitle
from PySide2 import QtWidgets, QtGui

import CONSTANTS
from CONSTANTS import get_resource
from MainWindow import MainWindow

if __name__ == "__main__":
    print("Starting Pepys")
    if sys.platform.lower().startswith("linux"):
        os.putenv("QT_QPA_PLATFORM", "xcb")
    if sys.platform.startswith("win32"):
        import ctypes
        myappid = 'dev.lukebriggs.pepys' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    if not os.path.isfile(get_resource("wordlist.txt")):
        with open(get_resource("wordlist.txt"), "w+") as file:
            file.write("")
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Pepys")
    app.setApplicationDisplayName("Pepys")
    app.setWindowIcon(QtGui.QIcon(get_resource("icons/appicons/icon.svg")))
    CONSTANTS.theme = "light" if QtWidgets.QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base).lightness() > 122 else "dark"
    CONSTANTS.light_palette = QtWidgets.QApplication.palette()
    setproctitle.setproctitle("Pepys")
    #Initialise and set size of main_window
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.setMinimumSize(640, 480)
    main_window.show()

    sys.exit(app.exec_())
