from __future__ import annotations
from PySide2 import QtWidgets, QtGui
from FileMenu import FileMenu
import typing
if typing.TYPE_CHECKING:
    from AppContext import AppContext


class CustomMenuBar(QtWidgets.QMenuBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, text_edit: QtWidgets.QTextEdit, ctx: AppContext) -> None:

        with open(ctx.get_resource("MenuBarStyle.qss"), 'r') as file:
            stylesheet = file.read()

        super().__init__()
        file_menu = FileMenu(text_edit, ctx)
        self.setStyleSheet(stylesheet)
        self.addMenu(file_menu)
