from __future__ import annotations
from PySide2 import QtWidgets, QtGui
import typing
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext

from OpenEntryButton import OpenEntryButton

class CustomMenuBar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, text_edit: QtWidgets.QTextEdit, ctx: AppContext) -> None:

        with open(ctx.get_resource("ToolbarStyle.qss"), 'r') as file:
            stylesheet = file.read()

        super().__init__()
        self.setStyleSheet(stylesheet)

        self.open_entry_button = OpenEntryButton(text_edit, ctx)

        self.addWidget(self.open_entry_button)
