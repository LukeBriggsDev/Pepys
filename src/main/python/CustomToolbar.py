from __future__ import annotations
from PySide2 import QtWidgets, QtGui
import typing
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext

from OpenEntryButton import OpenEntryButton
from FavoriteButton import FavoriteButton
from PreviewButton import PreviewButton
from EditPane import EditPane
from ViewPane import ViewPane
from HelpButton import HelpButton

class CustomToolbar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, edit_pane: EditPane, view_pane: ViewPane, ctx: AppContext) -> None:

        with open(ctx.get_resource("ToolbarStyle.qss"), 'r') as file:
            stylesheet = file.read()

        super().__init__()
        self.setStyleSheet(stylesheet)

        self.open_entry_button = OpenEntryButton(edit_pane, ctx)
        self.favorite_button = FavoriteButton(edit_pane, ctx)
        self.preview_button = PreviewButton(edit_pane, view_pane, ctx)
        self.about_button = HelpButton(ctx)

        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.preview_button)
        self.addWidget(self.about_button)


