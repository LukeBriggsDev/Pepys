from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from CONSTANTS import get_resource
from ExportWindow import ExportWindow

if typing.TYPE_CHECKING:
    from main import AppContext


class ExportButton(QtWidgets.QPushButton):
    """Button for opening export dialog"""
    def __init__(self):
        """Constructor
        :param ctx: AppContext containing global methods for accessing resources
        """
        super().__init__()
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(get_resource("icons/export.svg")))
        self.setToolTip("Export")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        # Create export dialog
        super().mousePressEvent(e)
        self.export_window = ExportWindow(self.window())
        # Disable current window
        self.parentWidget().parentWidget().setFocusProxy(self.export_window)
        self.parentWidget().parentWidget().setDisabled(True)
        self.export_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.export_window.show()
