from __future__ import annotations

import os
import sys
import typing
from datetime import date

from PyQt5 import QtWidgets, QtGui, QtCore

from ColorParser import *
from CustomToolbar import CustomToolbar
from EditPane import EditPane
from WebView import WebView

if typing.TYPE_CHECKING:
    pass

from CONSTANTS import get_resource

class MainWindow(QtWidgets.QWidget):
    """Main application window."""

    def __init__(self) -> None:
        """Initialise main window
        """
        super().__init__()
        self.date_opened = date.today()
        self.refresh_stylesheet()



        # Load config
        config_file = get_resource("config.json")
        with open(config_file, "r") as file:
            config_dict = json.loads(file.read())

        # Folder is not an absolute folder
        try:
            if not (config_dict['diary_directory'][0] == '/' or config_dict['diary_directory'][1] == ':') or not os.path.exists(config_dict['diary_directory']):
                self.select_diary_directory()
        except IndexError:
            self.select_diary_directory()

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

            config_dict["diary_directory"] = file_dialog.getExistingDirectory(self,
                                                    "Please select a directory to store your journal files",
                                                    "")

        # Cancel has been clicked
        if config_dict["diary_directory"] == "":
            if os.path.exists(old_dir):
                config_dict["diary_directory"] = old_dir
            else:
                exit(0)
        with open(config_file, "w") as file:
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
        self.edit_pane.open_file_from_date(date.fromisoformat(self.edit_pane.current_file_date))

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