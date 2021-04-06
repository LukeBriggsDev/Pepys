from __future__ import annotations
import sys
from enum import Enum

import mistune
import regex
from PySide2 import QtWidgets, QtGui
from fbs_runtime import PUBLIC_SETTINGS
from fbs_runtime.application_context.PySide2 import ApplicationContext
import os
import CodeSyntaxHighlighter
from EditPane import EditPane
from ViewPane import ViewPane
from CustomMenuBar import CustomMenuBar
import json
import datetime
from datetime import date
import typing

if typing.TYPE_CHECKING:
    from AppContext import AppContext


class MainWindow(QtWidgets.QWidget):
    """Main application window."""

    def __init__(self, ctx: AppContext) -> None:
        """Initialise main window

        :param ctx: Current ApplicationContext
        """
        super().__init__()

        # Load stylesheet
        filename = ctx.get_resource("styles.qss")
        with open(filename, "r") as file:
            stylesheet = file.read()

        self.setStyleSheet(stylesheet)

        # Load config
        filename = ctx.get_resource("config.json")
        with open(filename, "r") as file:
            self.CONFIG = json.loads(file.read())

        # filename = self.CONFIG["diary_directory"] + date.today().strftime("%Y-%m-%d")
        # with open(filename, "r") as file:
        #     print(file.read())

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # Edit pane
        self.edit_pane = EditPane(ctx)
        # Menu bar and adding edit pane underneath
        self.menu_bar = CustomMenuBar(self.edit_pane)
        self.layout.addWidget(self.menu_bar)
        self.layout.addWidget(self.edit_pane)
        # View pane
        self.view_pane = ViewPane(ctx)
        self.view_pane.setVisible(False)
        self.layout.addWidget(self.view_pane)
        # Switch pane button
        self.switch_pane_button = QtWidgets.QPushButton("Switch Pane")
        self.switch_pane_button.clicked.connect(self.switch_pane)
        self.layout.addWidget(self.switch_pane_button)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Perform any changes necessitated by window resize

        :param event: QResizeEvent that caused invocation
        """

        # Perform resize events on edit and view pane
        self.edit_pane.update_size(self.width())
        self.view_pane.update_size(self.width())

        #


    def switch_pane(self) -> None:
        self.edit_pane.setVisible(not self.edit_pane.isVisible())
        self.edit_pane.update_size(self.width())
        self.view_pane.update_size(self.width())

        self.view_pane.setHtml(
            mistune.markdown(self.edit_pane.toPlainText(), renderer=CodeSyntaxHighlighter.HighlightRenderer()))
        html = self.view_pane.toHtml().replace("<img ", f'<img width="{self.view_pane.width() * 0.5}" ')
        file_path_pattern = regex.compile('(?<=src=")\S*(?=")')
        filepaths = [filepath.group() for filepath in regex.finditer(file_path_pattern, self.view_pane.toHtml())]

        for filepath in filepaths:
            if filepath[0] != "/" or filepath[1] != ":":
                # Replace relative file paths
                # TODO: Maybe need to make directory separators agnostic for windows
                html = html.replace(filepath,
                                    os.path.join("/".join(self.edit_pane.current_file.split("/")[:-1]), filepath))

        self.view_pane.setHtml(html)
        self.view_pane.setVisible(not self.view_pane.isVisible())
