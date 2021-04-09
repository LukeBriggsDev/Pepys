from __future__ import annotations
import sys
from enum import Enum
from ColorParser import *
import mistune
import regex
from PySide2 import QtWidgets, QtGui, QtCore
from fbs_runtime import PUBLIC_SETTINGS
from fbs_runtime.application_context.PySide2 import ApplicationContext
import os
import HTMLRenderer
from EditPane import EditPane
from ViewPane import ViewPane
from CustomToolbar import CustomToolbar
import json
import datetime
from datetime import date
import typing
from num2words import num2words
import locale

if typing.TYPE_CHECKING:
    from AppContext import AppContext


class MainWindow(QtWidgets.QWidget):
    """Main application window."""

    def __init__(self, ctx: AppContext) -> None:
        """Initialise main window

        :param ctx: Current ApplicationContext
        """
        super().__init__()
        self.ctx = ctx

        self.date_opened = date.today()
        self.original_stylesheet = parse_stylesheet(ctx.get_resource("styles.qss"), ctx.get_resource("colors.json"), ctx.get_resource("config.json"))

        self.setStyleSheet(self.original_stylesheet)

        # Load config
        config_file = ctx.get_resource("config.json")
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
        self.edit_pane = EditPane(ctx)

        # View pane
        self.view_pane = ViewPane(ctx)
        self.view_pane.setVisible(False)

        # Menu bar and adding panes underneath
        self.tool_bar = CustomToolbar(self.edit_pane, self.view_pane, self.ctx)
        self.layout.addWidget(self.tool_bar)
        self.layout.addWidget(self.edit_pane)
        self.layout.addWidget(self.view_pane)



        self.edit_pane.open_file_from_date(date.today())


    def select_diary_directory(self):
        """Request user to select a directory and set it to diary_directory in config
        """
        # TODO: Maybe change so only create folder on first save
        config_file = self.ctx.get_resource("config.json")
        with open(config_file, "r") as file:
            config_dict = json.loads(file.read())
            file_dialog = QtWidgets.QFileDialog()

            config_dict["diary_directory"] = file_dialog.getExistingDirectory(self,
                                                    "Please select a directory to store your journal files",
                                                    "")

        if config_dict["diary_directory"] == "":
            exit(0)
        else:
            with open(config_file, "w") as file:
                file.write(json.dumps(config_dict, sort_keys=True, indent=4))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Perform any changes necessitated by window resize

        :param event: QResizeEvent that caused invocation
        """

        # Increase width of scroll bar left border to create a margin 25% width of the main window.
        margin_scale = 1 / 4
        scroll_bar_width = 4
        self.edit_pane.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {"
            f"width: {self.width() * margin_scale + scroll_bar_width};"
            f"border-left-width: {str(self.width() * margin_scale - scroll_bar_width)}px ;"
            "}")

        self.view_pane.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {"
            f"width: {self.width() * margin_scale + scroll_bar_width};"
            f"border-left-width: {str(self.width() * margin_scale - scroll_bar_width)}px ;"
            "}"
        )

        # Increase left border of the QTextEdit pane to create a left margin 25% width of the main window
        self.edit_pane.setStyleSheet(
                           "QTextEdit { "
                           f"border-left-width: {self.width() * margin_scale} px;"
                           "}")

        # Increase left border of the QTextEdit pane to create a left margin 25% width of the main window

        self.view_pane.setStyleSheet(
                           f"border-left-width: {self.width() * margin_scale} px;"
                           )

        self.view_pane.update_size(self.width())


    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        sys.exit()
