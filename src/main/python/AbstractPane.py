from __future__ import annotations
import typing
import re
import json

from PySide2 import QtWidgets, QtGui, QtCore
from ColorParser import *

if typing.TYPE_CHECKING:
    from AppContext import AppContext


class AbstractPane(QtWidgets.QTextEdit):
    """Contain abstract methods and attributes for use by both the EditPane and ViewPane"""

    def __init__(self, ctx: AppContext) -> None:
        """Initialise a QTextEdit and apply attributes required at load time.

        :param ctx: current ApplicationContext, used to get stylesheet resource
        """
        super().__init__()

        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

        #self.setStyleSheet(parse_stylesheet(ctx.get_resource("PaneStyle.qss"), ctx.get_resource("colors.json"), ctx.get_resource("config.json")))
        self.setVerticalScrollBarPolicy(self.verticalScrollBarPolicy().ScrollBarAlwaysOn)

    def update_size(self, new_frame_width: int) -> None:
        """Updates style based on a given frame size. To be called when the window changes size.

        :param new_frame_width: the frame width to style to
        """

        # Increase width of scroll bar left border to create a margin 25% width of the main window.
        margin_scale = 1 / 4
        scroll_bar_width = 4
        self.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {"
            f"width: {new_frame_width * margin_scale + scroll_bar_width};"
            f"border-left-width: {str(new_frame_width * margin_scale - scroll_bar_width)}px ;"
            "}")

        # Increase left border of the QTextEdit pane to create a left margin 25% width of the main window
        self.setStyleSheet(self.styleSheet() +
                           "QTextEdit { "
                           f"border-left-width: {new_frame_width * margin_scale} px;"
                           "}")

    def enterEvent(self, event: QtCore.QEvent) -> None:
        """"Override base QTextEdit method, called when mouse is over TextEdit

        :param event: the QEvent that caused the invocation
        """

        self.verticalScrollBar().setVisible(True)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        """"Override base QTextEdit method, called when mouse leaves TextEdit

        :param event: the QEvent that caused the invocation
        """

        self.verticalScrollBar().setVisible(False)
