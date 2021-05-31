from PyQt5 import QtGui, QtWidgets, QtCore
from EditPane import EditPane
from WebView import WebView
import datetime
import calendar
import os
import json

class EntryExplorer(QtWidgets.QWidget):
    def __init__(self, edit_pane, web_view):
        """Constructor
        :param edit_pane: EditPane to open the new file in
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.web_view = web_view
        self.setWindowFlag(QtCore.Qt.Dialog)

        date = self.edit_pane.current_file_date.split("-")

        self.setSelectedDate(QtCore.QDate(
            int(date[0]), int(date[1]), int(date[2])
        ))

        #self.selectionChanged.connect(self.selection_changed_handler)

        self.setMinimumSize(480, 480)
        self.setMaximumSize(480, 480)
        self.setWindowTitle("Calendar")

        main_layout = QtWidgets.QVBoxLayout()

        # Year/month select
        toolbar = QtWidgets.QToolBar()
        month_combo = QtWidgets.QComboBox()
        month_combo.addItems(calendar.month_name[1:])
        month_combo.setCurrentIndex(self.selected_date.month() - 1)
        year_entry = QtWidgets.QSpinBox()
        year_entry.setMinimum(0)
        year_entry.setMaximum(9999)
        toolbar.addWidget(month_combo)
        toolbar.addWidget(year_entry)

        # Calendar grid
        grid_layout = QtWidgets.QGridLayout()
        cal = calendar.monthcalendar(self.selected_date.year(), self.selected_date.month())
        for week in range(len(cal)):
            for day in range(len(cal[week])):
                print(cal[week][day])
                button = QtWidgets.QPushButton()
                button.setContentsMargins(0, 0, 0, 0)
                button.setText(str(cal[week][day]))
                grid_layout.addWidget(button, week, day)
        grid_layout.setSpacing(0)

        main_layout.addWidget(toolbar)
        main_layout.addLayout(grid_layout)

        self.setLayout(main_layout)
    def setSelectedDate(self, date: QtCore.QDate):
        self.selected_date = date

