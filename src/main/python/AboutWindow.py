from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from datetime import date
from ColorParser import *
import typing
if typing.TYPE_CHECKING:
    from main import AppContext
import os
import json

class AboutWindow(QtWidgets.QWidget):
    """Window showing basic info, licenses, and version"""
    def __init__(self, main_window, ctx: AppContext):
        """Constructor
        :param main_window:
        """
        super().__init__()
        self.main_window = main_window
        self.setMaximumSize(360, 360)
        self.setMinimumSize(360, 360)
        self.setWindowFlag(QtGui.Qt.Dialog)
        self.about_label = QtWidgets.QLabel()

        # Link settings
        self.about_label.setTextFormat(QtGui.Qt.RichText)
        self.about_label.setTextInteractionFlags(QtGui.Qt.TextBrowserInteraction)
        self.about_label.setOpenExternalLinks(True)

        #Formatting
        self.about_label.setAlignment(QtGui.Qt.AlignCenter)
        self.about_label.setWordWrap(True)
        self.about_label.setText(
            f'<img src="{ctx.get_resource("icons/icon-mac.svg")}"/>'
            '<p style="font-size: 11pt">'
            '<b>Pepys:</b><br>'
            'A Straightforward Markdown Journal<br>'
            '<a href="https://lukebriggs.dev">©Luke Briggs</a><br><br><br>'
            '</p>'
            
            '<p style="font-size: 8pt">'
            '<a href="https://rsms.me/inter/">Inter</a> provided under '
            '<a href ="https://choosealicense.com/licenses/ofl-1.1/">SIL Open Font License 1.1</a><br>'
            '<a href = "https://fonts.google.com/specimen/Roboto+Mono">Roboto Mono</a> provided under'
            '<a href = "https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a>'
            '<br><br><br>'
            f'version {ctx.version}'
            '</p>'

        )
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.about_label)
        self.setStyleSheet(parse_stylesheet(ctx.get_resource("styles.qss"), ctx.get_resource("colors.json"), ctx.get_resource("config.json")))


    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        self.main_window.setFocusPolicy(QtGui.Qt.StrongFocus)
        self.main_window.setDisabled(False)

