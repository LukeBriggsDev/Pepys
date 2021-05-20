import sys
import os
import pathlib
import setproctitle
from PySide2 import QtWidgets, QtGui, QtCore
from CONSTANTS import get_resource
import CONSTANTS

from MainWindow import MainWindow

if __name__ == "__main__":
    print("Starting Pepys")
    if sys.platform.lower().startswith("linux"):
        os.putenv("QT_QPA_PLATFORM", "xcb")
    if not os.path.isfile(pathlib.Path.home().as_posix()+"/.pepys/wordlist.txt"):
        with open(pathlib.Path.home().as_posix()+"/.pepys/wordlist.txt", "w+") as file:
            file.write("")
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Pepys")
    app.setApplicationDisplayName("Pepys")
    app.setWindowIcon(QtGui.QIcon(get_resource("icons/appicons/icon.svg")))
    CONSTANTS.theme = "light" if QtWidgets.QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base).lightness() > 122 else "dark"
    print(QtWidgets.QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base).lightness())
    setproctitle.setproctitle("Pepys")
    #Initialise and set size of main_window
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.setMinimumSize(640, 480)
    main_window.show()
    version = "0.3.0"

    sys.exit(app.exec_())
