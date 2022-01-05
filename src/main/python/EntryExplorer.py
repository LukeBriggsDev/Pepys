"""
    Copyright (C) 2021  Luke Briggs <lukebriggs02@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from PyQt6 import QtGui, QtWidgets, QtCore
from EditPane import EditPane
from WebView import WebView
import calendar

class EntryExplorer(QtWidgets.QWidget):
    def __init__(self, edit_pane, web_view):
        """Constructor
        :param edit_pane: EditPane to open the new file in
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.web_view = web_view
        self.setWindowFlag(QtCore.Qt.WindowType.Dialog)

        date = self.edit_pane.current_file_date.split("-")

        self.setSelectedDate(QtCore.QDate(
            int(date[0]), int(date[1]), int(date[2])
        ))


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

