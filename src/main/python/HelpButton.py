from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
import mistune
import regex
import CodeSyntaxHighlighter
import os
import json
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext
    from EditPane import EditPane
    from ViewPane import ViewPane

class HelpButton(QtWidgets.QPushButton):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/question.svg")))
        self.setToolTip("About")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)