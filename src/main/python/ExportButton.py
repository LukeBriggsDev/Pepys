from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from ExportWindow import ExportWindow

if typing.TYPE_CHECKING:
    from main import AppContext


class ExportButton(QtWidgets.QPushButton):
    """Button for opening export dialog"""
    def __init__(self, ctx: AppContext):
        """Constructor
        :param ctx: AppContext containing global methods for accessing resources
        """
        super().__init__()
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/export.svg")))
        self.setToolTip("Export")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        # Create export dialog
        super().mousePressEvent(e)
        self.export_window = ExportWindow(self.window(), self.ctx)
        # Disable current window
        self.parentWidget().parentWidget().setFocusProxy(self.export_window)
        self.parentWidget().parentWidget().setDisabled(True)
        self.export_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.export_window.show()
