from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui, QtCore

from WebView import WebView

if typing.TYPE_CHECKING:
    pass

from CalendarButton import CalendarButton
from FavoriteButton import FavoriteButton
from PreviewButton import PreviewButton
from EditPane import EditPane
from AboutButton import AboutButton
from ThemeSwitchButton import ThemeSwitchButton
from ExportButton import ExportButton
from CONSTANTS import get_resource
import CONSTANTS

class CustomToolbar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, edit_pane: EditPane, web_view: WebView) -> None:
        """Constructor
        :param edit_pane: EditPane holding currently editing document
        :param web_view: WebView to hold the output of the edit pane
        """

        super().__init__()
        # Initialise buttons
        self.open_entry_button = CalendarButton(edit_pane)
        self.favorite_button = FavoriteButton(edit_pane)
        self.preview_button = PreviewButton(edit_pane, web_view)
        self.about_button = AboutButton()
        self.theme_switch_button= ThemeSwitchButton()
        self.export_button = ExportButton()

        # Add buttons to layout
        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        #self.addWidget(self.export_button)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.preview_button)
        self.addWidget(self.theme_switch_button)
        self.addWidget(self.about_button)


    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change button icons to match theme
        if event.type() is QtCore.QEvent.Type.StyleChange:
            self.open_entry_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["open_entry"][CONSTANTS.theme])))
            self.favorite_button.refresh_icon()
            self.preview_button.refresh_icon()
            self.about_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["about"][CONSTANTS.theme])))
            self.theme_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["theme_switch"][CONSTANTS.theme])))
            self.export_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["export"][CONSTANTS.theme])))
