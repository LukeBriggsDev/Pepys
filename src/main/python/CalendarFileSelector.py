from __future__ import annotations

import typing
from datetime import date

from PySide2 import QtWidgets, QtGui, QtCore

from CONSTANTS import get_resource
import CONSTANTS
from ColorParser import *
from EditPane import EditPane
from WebView import WebView

if typing.TYPE_CHECKING:
    pass
import json


class CalendarFileSelector(QtWidgets.QCalendarWidget):
    """Calendar widget for selecting the journal entry to edit"""
    def __init__(self, edit_pane: EditPane, web_view: WebView):
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

        self.selectionChanged.connect(self.selection_changed_handler)

        self.layout = QtWidgets.QVBoxLayout()
        self.setVerticalHeaderFormat(self.NoVerticalHeader)
        self.setMinimumSize(480, 480)
        self.setMaximumSize(480, 480)
        self.setWindowTitle("Calendar")

        self.setStyleSheet("""
        QMenu { 
            font-size:16px; 
            width: 150px; 
            left: 20px; 
            background-color: palette(base);
        }
        QWidget{
            background-color: palette(base)
        }
        QToolButton {
            icon-size: 24px, 24px;
            background-color: palette(base);
        }
        QAbstractItemView {
            selection-background-color: rgb(255, 174, 0);
        }
        QToolButton::menu-arrow {
        }
        QToolButton::menu-button {
        }
        QToolButton::menu-indicator{
            width: 50px;
        }
        QToolButton::menu-indicator:pressed, QToolButton::menu-indicator:open{
            top:10px; 
            left: 10px;
        }
        QListView {
        background-color:white;
        }
        QSpinBox {
            width:200px; 
            border-width: 2px;
        }
        QSpinBox::up-button { 
            subcontrol-origin: border;
            subcontrol-position: top right; 
            width:50px; border-image: url(icons:arrow_up_n.png);
        }
        QSpinBox::down-button {
            subcontrol-origin: border; 
            subcontrol-position: bottom right;
            border-width: 1px; 
            width:10px;
            }
        QSpinBox::down-arrow { 
            width:6px; 
            height:6px;
        image: url(icons:arrow_down_n.png); 
        }
""")

        # Set format of how favorites appear in calendar
        favorite_format = QtGui.QTextCharFormat()
        favorite_brush = QtGui.QBrush()
        favorite_brush.setColor(QtGui.QColor.fromRgb(255, 228, 0))
        favorite_format.setBackground(favorite_brush)
        favorite_brush.setColor(QtGui.QColor.fromRgb(33, 33, 33))
        favorite_format.setForeground(favorite_brush)

        prev_month_button = self.findChild(QtWidgets.QToolButton, "qt_calendar_prevmonth")
        next_month_button = self.findChild(QtWidgets.QToolButton, "qt_calendar_nextmonth")
        prev_month_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["left_arrow"][CONSTANTS.theme])))
        next_month_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["right_arrow"][CONSTANTS.theme])))

        with open(get_resource("config.json")) as file:
            for day in json.loads(file.read())["favorites"]:
                formatted_date = [int(x) for x in day.split("-")]
                self.setDateTextFormat(QtCore.QDate(formatted_date[0], formatted_date[1], formatted_date[2]), favorite_format)


    def selection_changed_handler(self) -> None:
        """Called when new date selected, opens the corresponding file in the edit pane"""
        self.edit_pane.open_file_from_date(date(self.selectedDate().year(),
                                                self.selectedDate().month(),
                                                self.selectedDate().day()))
        self.web_view.refresh_page()

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        # Re-enable the window of the edit=pane
        self.edit_pane.parentWidget().setFocusPolicy(QtCore.Qt.StrongFocus)
        self.edit_pane.parentWidget().setDisabled(False)


