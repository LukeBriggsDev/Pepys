from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from AboutWindow import AboutWindow
from CONSTANTS import get_resource

if typing.TYPE_CHECKING:
    pass


class AboutButton(QtWidgets.QPushButton):
    """Button to display about dialog"""
    def __init__(self):
        """Constructor
        :param ctx: AppContext containing global variables and functions
        """
        super().__init__()
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(get_resource("icons/question.svg")))
        self.setToolTip("About")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        # Create about dialog
        self.about_window = AboutWindow(self.window())

        # Disable main window
        self.parentWidget().parentWidget().setFocusProxy(self.about_window)
        self.parentWidget().parentWidget().setDisabled(True)
        self.about_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.about_window.show()
