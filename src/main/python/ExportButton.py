from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
import regex
import HTMLRenderer
import os
import json
from CalendarFileSelector import CalendarFileSelector
from AboutWindow import AboutWindow
from ExportWindow import ExportWindow
if typing.TYPE_CHECKING:
    from main import AppContext
    from EditPane import EditPane
    from ViewPane import ViewPane

class ExportButton(QtWidgets.QPushButton):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/export.svg")))
        self.setToolTip("Export")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.export_window = ExportWindow(self.window(), self.ctx)
        self.parentWidget().parentWidget().setFocusProxy(self.export_window)
        self.parentWidget().parentWidget().setDisabled(True)
        self.export_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.export_window.show()
