from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from AboutWindow import AboutWindow

if typing.TYPE_CHECKING:
    from main import AppContext


class AboutButton(QtWidgets.QPushButton):
    """Button to display about dialog"""
    def __init__(self, ctx: AppContext):
        """Constructor
        :param ctx: AppContext containing global variables and functions
        """
        super().__init__()
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/question.svg")))
        self.setToolTip("About")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        # Create about dialog
        self.about_window = AboutWindow(self.window(), self.ctx)

        # Disable main window
        self.parentWidget().parentWidget().setFocusProxy(self.about_window)
        self.parentWidget().parentWidget().setDisabled(True)
        self.about_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.about_window.show()
