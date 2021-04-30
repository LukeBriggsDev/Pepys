from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from CONSTANTS import get_resource
from CalendarFileSelector import CalendarFileSelector

if typing.TYPE_CHECKING:
    from EditPane import EditPane

class CalendarButton(QtWidgets.QPushButton):
    """Button for opening calendar dialog"""
    def __init__(self, edit_pane: EditPane):
        """Constructor
        :param edit_pane: EditPane where the file will be opened
        :param ctx: AppContext containing global function for accessing resources
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.setMinimumSize(32, 32)
        self.setMaximumSize(32, 32)
        self.setToolTip("Open Entry")
        self.setWhatsThis("Click this to select an entry via a calendar")
        self.setIcon(QtGui.QIcon(get_resource("icons/calendar.svg")))

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.open_date_picker()

    def open_date_picker(self) -> None:
        """Open calendar dialog and disable main window"""
        self.date_dialog = CalendarFileSelector(self.edit_pane)
        self.parentWidget().parentWidget().setFocusProxy(self.date_dialog)
        self.parentWidget().parentWidget().setDisabled(True)
        self.date_dialog.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.date_dialog.show()
