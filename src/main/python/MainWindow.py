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
from __future__ import annotations

import os
import sys
import typing
from datetime import date

from PyQt6 import QtWidgets, QtGui, QtCore

from ColorParser import *
from CustomToolbar import CustomToolbar
from EditPane import EditPane
from WebView import WebView
from Crypto import generateVerificationStringFromPassword, Crypto
from shutil import which
from pypandoc.pandoc_download import download_pandoc

if typing.TYPE_CHECKING:
    pass

from CONSTANTS import get_resource

class MainWindow(QtWidgets.QWidget):
    """Main application window."""

    def __init__(self) -> None:
        """Initialise main window
        """
        super().__init__()
        if which("pandoc") is None and sys.platform.startswith("win32"):
            os.environ.setdefault("PYPANDOC_PANDOC", get_resource("pandoc-2.13/pandoc.exe"))
        self.date_opened = date.today()
        self.refresh_stylesheet()



        # Load config
        config_file = get_resource("config.json")
        with open(config_file, "r") as file:
            config_dict = json.loads(file.read())

        self.no_journal_dialog = QtWidgets.QMessageBox()
        self.no_journal_dialog.setText("No journal directory configured")
        self.no_journal_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Close |
                                                  QtWidgets.QMessageBox.StandardButton.Open)
        self.no_journal_dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Open)

        # Folder is not an absolute folder
        try:
            if not (config_dict['diary_directory'][0] == '/' or config_dict['diary_directory'][1] == ':') or not os.path.exists(config_dict['diary_directory']):
                answer = self.no_journal_dialog.exec()
                if answer == QtWidgets.QMessageBox.StandardButton.Open:
                    self.select_diary_directory()
                else:
                    exit(0)
        except IndexError:
            answer = self.no_journal_dialog.exec()
            if answer == QtWidgets.QMessageBox.StandardButton.Open:
                self.select_diary_directory()
            else:
                exit(0)

        if ("password_hash" in config_dict):
            password_ok = False
            while(not password_ok):
                password, ok = QtWidgets.QInputDialog.getText(self, "Enter Password", "Please enter your encryption password: ", QtWidgets.QLineEdit.EchoMode.Password)
                if not ok:
                    exit(0)
                hash = generateVerificationStringFromPassword(password)
                if (hash == config_dict["password_hash"]):
                    password_ok = True
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Wrong password. Try again.", QtWidgets.QMessageBox.StandardButton.Ok)
            Crypto(password) # Initialize crypto key
            

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Edit pane
        self.edit_pane = EditPane()

        self.web_view = WebView(self.edit_pane)

        # Menu bar and adding panes underneath
        self.tool_bar = CustomToolbar(self, self.edit_pane, self.web_view)

        self.layout.addWidget(self.tool_bar)
        self.layout.addWidget(self.edit_pane)
        self.layout.addWidget(self.web_view)

        self.edit_pane.open_file_from_date(date.today())

    def select_diary_directory(self):
        """Request user to select a directory and set it to diary_directory in config
        """
        # TODO: Maybe change so only create folder on first save
        config_file = get_resource("config.json")
        with open(config_file, "r") as file:
            config_dict = json.loads(file.read())
            file_dialog = QtWidgets.QFileDialog()
            old_dir = config_dict["diary_directory"]

            # Need non-native file in flatpak to get correct directory
            if sys.platform.startswith("linux"):
                config_dict["diary_directory"] = file_dialog.getExistingDirectory(self,
                                                        "Please select a directory to store your journal files",
                                                        "", QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.DontUseNativeDialog)
            else:
                config_dict["diary_directory"] = file_dialog.getExistingDirectory(self,
                                                                                  "Please select a directory to store your journal files",
                                                                                  "")
            print(config_dict["diary_directory"])

        # Cancel has been clicked
        if config_dict["diary_directory"] == "":
            if os.path.exists(old_dir):
                config_dict["diary_directory"] = old_dir
            else:
                exit(0)
        with open(config_file, "w") as file:
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
        try:
            self.edit_pane.open_file_from_date(date.fromisoformat(self.edit_pane.current_file_date))
        except AttributeError:
            print("First time boot")

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Perform any changes necessitated by window resize

        :param event: QResizeEvent that caused invocation
        """
        # Increase width of scroll bar left border to create a margin 25% width of the main window.
        self.edit_pane.set_margins()

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        sys.exit()


    def refresh_stylesheet(self):
        self.setStyleSheet("""
        MainWindow{
            background-color: palette(base);
            border: 0px solid palette(base);
        }
        MainWindow:!active{
            background-color: palette(base);
        }
        MainWindow EditPane:!active{
            background-color: palette(base);
        }
        """)