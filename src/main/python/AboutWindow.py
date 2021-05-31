from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui, QtCore

from ColorParser import *

if typing.TYPE_CHECKING:
    pass
import CONSTANTS
from CONSTANTS import get_resource


class AboutWindow(QtWidgets.QWidget):
    """Window showing basic info, licenses, and version"""
    def __init__(self, main_window):
        """Constructor
        :param main_window:
        """
        super().__init__()
        self.main_window = main_window
        self.setMaximumSize(360, 360)
        self.setMinimumSize(360, 360)
        self.setWindowFlag(QtCore.Qt.Dialog)
        self.about_label = QtWidgets.QLabel()

        # Link settings
        self.about_label.setTextFormat(QtCore.Qt.RichText)
        self.about_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.about_label.setOpenExternalLinks(True)

        #Formatting
        self.about_label.setAlignment(QtCore.Qt.AlignCenter)
        self.about_label.setWordWrap(True)
        self.about_label.setText(
            f'<img src="{get_resource("icons/appicons/hires/128x128/apps/dev.lukebriggs.pepys.png")}"/>'
            '<p style="font-size: 11pt">'
            '<b>Pepys:</b><br>'
            'A Straightforward Markdown Journal<br><br>'
            '<a style="text-decoration: none; color: rgb(0,125,225);" '
            'href="https://pandoc.org/MANUAL.html#pandocs-markdown">Syntax Documentation</a><br><br>'
            '<a style="text-decoration: none; color: rgb(0,125,225);" '
            '   href="https://lukebriggs.dev">©Luke Briggs</a><br>'
            '</p>'
            f'version {CONSTANTS.version}'
            '</p>'

        )
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.about_label)
        self.setStyleSheet("""    
        text-align: center;
        background-color: palette(window);
        color: palette(text);
    """)
        self.setWindowTitle("About")


    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        self.main_window.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.main_window.setDisabled(False)

