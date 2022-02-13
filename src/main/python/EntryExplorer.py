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

from CalendarFileSelector import CalendarFileSelector
from SearchWidget import SearchWidget

class EntryExplorer(QtWidgets.QTabWidget):
    def __init__(self, edit_pane, web_view):
        """Constructor
        :param edit_pane: EditPane to open the new file in
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.web_view = web_view
        self.setWindowFlag(QtCore.Qt.WindowType.Dialog)

        self.setMinimumSize(640, 660)
        self.setMaximumSize(640, 660)
        self.setWindowTitle("Entry Explorer")

        self.calendar = CalendarFileSelector(self.edit_pane, self.web_view)
        self.search = SearchWidget(self.edit_pane, self.web_view)

        self.addTab(self.calendar, "Calendar")
        self.addTab(self.search, "Search")
        palette = QtWidgets.QApplication.palette()
        self.tabBar().setTabTextColor(0, palette.text().color())
        self.tabBar().setTabTextColor(1, palette.text().color())
        self.setStyleSheet(
            """
            QWidget {
                background: palette(base);
                border: none;
            }
            QTabBar::tab {
                background: palette(button);
                border: 1px solid palette(mid);
                padding: 4px;
            } 
            QTabBar::tab:selected { 
                background: palette(dark); 
            } 
            """
        )


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.search.close()
        self.calendar.close()
        self.edit_pane.parentWidget().tool_bar.setEnabled(True)