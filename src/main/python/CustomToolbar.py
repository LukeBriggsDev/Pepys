from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
from ColorParser import *
from CalendarFileSelector import CalendarFileSelector
from WebView import WebView
if typing.TYPE_CHECKING:
    from main import AppContext

import json
import regex

from OpenEntryButton import OpenEntryButton
from FavoriteButton import FavoriteButton
from PreviewButton import PreviewButton
from EditPane import EditPane
from HelpButton import HelpButton
from ThemeSwitchButton import ThemeSwitchButton
from ExportButton import ExportButton

class CustomToolbar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, edit_pane: EditPane, web_view: WebView, ctx: AppContext) -> None:

        super().__init__()
        self.ctx = ctx

        self.open_entry_button = OpenEntryButton(edit_pane, ctx)
        self.favorite_button = FavoriteButton(edit_pane, ctx)
        self.preview_button = PreviewButton(edit_pane, web_view, ctx)
        self.about_button = HelpButton(ctx)
        self.theme_switch_button= ThemeSwitchButton(ctx)
        self.export_button = ExportButton(ctx)

        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        self.addWidget(self.export_button)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.preview_button)
        self.addWidget(self.theme_switch_button)
        self.addWidget(self.about_button)


    def changeEvent(self, event:QtCore.QEvent) -> None:
        if event.type() is QtCore.QEvent.Type.StyleChange:
            self.open_entry_button.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["open_entry"][self.ctx.theme])))
            self.favorite_button.refresh_icon()
            self.preview_button.refresh_icon()
            self.about_button.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["about"][self.ctx.theme])))
            self.theme_switch_button.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["theme_switch"][self.ctx.theme])))
            self.export_button.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["export"][self.ctx.theme])))
