from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from datetime import date
import os


class CalendarFileSelector(QtWidgets.QCalendarWidget):
    def __init__(self, edit_pane: EditPane):
        super().__init__()
        self.edit_pane = edit_pane
        date = (os.path.split(self.edit_pane.current_file))[1][:-3].split("-")
        self.setSelectedDate(QtCore.QDate(
            int(date[0]), int(date[1]), int(date[2])
        ))
        self.selectionChanged.connect(self.selection_changed_handler)

    def selection_changed_handler(self):
        self.edit_pane.open_file_from_date(date(self.selectedDate().year(),
                                                self.selectedDate().month(),
                                                self.selectedDate().day()))

