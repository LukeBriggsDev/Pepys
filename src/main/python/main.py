import sys
import os
import pathlib
import setproctitle
from PyQt5 import QtWidgets, QtGui
from CONSTANTS import get_resource

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
    setproctitle.setproctitle("Pepys")
    #Initialise and set size of main_window
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.setMinimumSize(640, 480)
    main_window.show()
    version = "0.3.0"

    sys.exit(app.exec_())
