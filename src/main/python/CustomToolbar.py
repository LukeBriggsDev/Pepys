from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
from ColorParser import *
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext

import json
import regex

from OpenEntryButton import OpenEntryButton
from FavoriteButton import FavoriteButton
from PreviewButton import PreviewButton
from EditPane import EditPane
from ViewPane import ViewPane
from HelpButton import HelpButton
from ThemeSwitchButton import ThemeSwitchButton

class CustomToolbar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, edit_pane: EditPane, view_pane: ViewPane, ctx: AppContext) -> None:

        super().__init__()
        self.ctx = ctx

        self.open_entry_button = OpenEntryButton(edit_pane, ctx)
        self.favorite_button = FavoriteButton(edit_pane, ctx)
        self.preview_button = PreviewButton(edit_pane, view_pane, ctx)
        self.about_button = HelpButton(ctx)
        self.theme_switch_button= ThemeSwitchButton(ctx)

        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.preview_button)
        self.addWidget(self.theme_switch_button)
        self.addWidget(self.about_button)


    def changeEvent(self, event:QtCore.QEvent) -> None:
        if event.type() is QtCore.QEvent.Type.StyleChange:
            with open(self.ctx.get_resource("config.json")) as config:
                theme = json.loads(config.read())["theme"]

            if theme == "light":
                color = "black"

            else:
                color = "white"

            with open(self.ctx.get_resource("icons/book.svg"), "r+") as icon:
                icon_file = icon.read()

            with open(self.ctx.get_resource("icons/book.svg"), "w+") as icon:
                icon.write(regex.sub(r'(?<=src=")\S*(?=")', color, icon_file))







