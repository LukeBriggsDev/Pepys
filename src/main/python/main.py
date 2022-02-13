"""
    Copyright (C) 2021  Luke Briggs <lukebriggs02@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re
import subprocess
import sys
import os
if sys.platform.lower().startswith("darwin"):
    os.environ["PYENCHANT_LIBRARY_PATH"] = subprocess.run(["command", "-v", "enchant-2"], capture_output=True).stdout.decode("utf-8").strip("\n")
if sys.platform.startswith('darwin'):
    # Set app name, if PyObjC is installed
    # Python 2 has PyObjC preinstalled
    # Python 3: pip3 install pyobjc-framework-Cocoa
    try:
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        if bundle:
            app_name = "Pepys"
            app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
            if app_info:
                app_info['CFBundleName'] = app_name
    except ImportError:
        pass
import pathlib
import enchant
import setproctitle
from PyQt6 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
app = QtWidgets.QApplication(sys.argv)
app.setApplicationName("Pepys")
app.setApplicationDisplayName("Pepys")
from CONSTANTS import get_resource
import CONSTANTS
from pypandoc.pandoc_download import download_pandoc
import pypandoc

from MainWindow import MainWindow

if __name__ == "__main__":
    if sys.platform.lower().startswith("linux"):
        os.putenv("QT_QPA_PLATFORM", "xcb")
    if sys.platform.startswith("win32"):
        import ctypes
        myappid = 'dev.lukebriggs.pepys' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    if sys.platform.lower().startswith("darwin"):
        os.putenv("QTWEBENGINE_CHROMIUM_FLAGS", "--single-process")

    if not os.path.isfile(get_resource("wordlist.txt")):
        with open(get_resource("wordlist.txt"), "w+") as file:
            file.write("")
    app.setWindowIcon(QtGui.QIcon(get_resource("icons/appicons/icon.svg")))
    CONSTANTS.theme = "light" if QtWidgets.QApplication.palette().color(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base).lightness() > 122 else "dark"
    if CONSTANTS.theme == "light":
        QtWidgets.QApplication.setPalette(CONSTANTS.light_palette)
    else:
        QtWidgets.QApplication.setPalette(CONSTANTS.Colors.getDarkpalette())
    setproctitle.setproctitle("Pepys")
    #Initialise and set size of main_window
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.setMinimumSize(640, 480)
    main_window.show()

    sys.exit(app.exec())
