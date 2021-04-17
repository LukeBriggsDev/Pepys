from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from datetime import date
from ColorParser import *
import typing
if typing.TYPE_CHECKING:
    from main import AppContext
import os
import json


class CalendarFileSelector(QtWidgets.QCalendarWidget):
    """Calendar widget for selecting the journal entry to edit"""
    def __init__(self, edit_pane: EditPane, ctx: AppContext):
        """Constructor
        :param edit_pane: EditPane to open the new file in
        :param ctx: AppContext with function to retrieve resources
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.setWindowFlag(QtGui.Qt.Dialog)

        date = self.edit_pane.current_file_date.split("-")
        self.setSelectedDate(QtCore.QDate(
            int(date[0]), int(date[1]), int(date[2])
        ))

        self.selectionChanged.connect(self.selection_changed_handler)

        self.layout = QtWidgets.QVBoxLayout()
        self.setVerticalHeaderFormat(self.NoVerticalHeader)
        self.setMinimumSize(480, 480)
        self.setMaximumSize(480, 480)
        self.setWindowTitle("Calendar")

        self.setStyleSheet(parse_stylesheet(ctx.get_resource("CalendarStyle.qss"), ctx.get_resource("colors.json"), ctx.get_resource("config.json")))

        # Set format of how favorites appear in calendar
        favorite_format = QtGui.QTextCharFormat()
        favorite_brush = QtGui.QBrush()
        favorite_brush.setColor(QtGui.QColor.fromRgb(255, 228, 0))
        favorite_format.setBackground(favorite_brush)
        favorite_brush.setColor(QtGui.QColor.fromRgb(33, 33, 33))
        favorite_format.setForeground(favorite_brush)

        with open(ctx.get_resource("config.json")) as file:
            for day in json.loads(file.read())["favorites"]:
                formatted_date = [int(x) for x in day.split("-")]
                self.setDateTextFormat(QtCore.QDate(formatted_date[0], formatted_date[1], formatted_date[2]), favorite_format)


    def selection_changed_handler(self) -> None:
        """Called when new date selected, opens the corresponding file in the edit pane"""
        self.edit_pane.open_file_from_date(date(self.selectedDate().year(),
                                                self.selectedDate().month(),
                                                self.selectedDate().day()))

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        # Re-enable the window of the edit=pane
        self.edit_pane.parentWidget().setFocusPolicy(QtGui.Qt.StrongFocus)
        self.edit_pane.parentWidget().setDisabled(False)


