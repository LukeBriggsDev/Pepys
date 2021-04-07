from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from datetime import date
import typing
if typing.TYPE_CHECKING:
    from AppContext import AppContext
import os


class CalendarFileSelector(QtWidgets.QCalendarWidget):
    def __init__(self, edit_pane: EditPane, ctx: AppContext):
        super().__init__()
        self.edit_pane = edit_pane
        date = (os.path.split(self.edit_pane.current_file))[1][:-3].split("-")
        self.setSelectedDate(QtCore.QDate(
            int(date[0]), int(date[1]), int(date[2])
        ))
        self.selectionChanged.connect(self.selection_changed_handler)
        self.layout = QtWidgets.QVBoxLayout()
        self.setVerticalHeaderFormat(self.NoVerticalHeader)
        self.setMinimumSize(480, 480)
        self.setMaximumSize(480, 480)
        self.setWindowTitle("Calendar")

        stylesheet = ctx.get_resource("CalendarStyle.qss")
        with open(stylesheet, 'r') as file:
            self.setStyleSheet(file.read())

        format = QtGui.QTextCharFormat()
        format.setFontFamily("IBM Plex Mono")
        self.setHeaderTextFormat(format)

    def selection_changed_handler(self):
        self.edit_pane.open_file_from_date(date(self.selectedDate().year(),
                                                self.selectedDate().month(),
                                                self.selectedDate().day()))


