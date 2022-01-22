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
from __future__ import annotations

import random
import typing
from datetime import date
from random import randint

from PyQt6 import QtWidgets, QtGui, QtCore

from CONSTANTS import get_resource
import CONSTANTS
from ColorParser import *
import datetime
from EditPane import EditPane
from WebView import WebView
from EntryFile import EntryFile

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
        self.setVerticalHeaderFormat(self.verticalHeaderFormat().NoVerticalHeader)
        self.setMinimumSize(640, 640)
        self.setMaximumSize(640, 640)
        self.setWindowTitle("Calendar")

        self.setStyleSheet("""
        QMenu { 
            font-size:16px; 
            width: 150px; 
            left: 20px; 
            background-color: palette(base);
        }
        QWidget{
            background-color: palette(base);
        }
        QToolButton {
            icon-size: 24px, 24px;
            background-color: palette(base);
            color: palette(text);
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
        QMenu::item:selected{
            background-color: palette(highlight);
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


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.edit_pane.parentWidget().tool_bar.setEnabled(True)

    def paintCell(self, painter: QtGui.QPainter, rect: QtCore.QRect, date: typing.Union[QtCore.QDate, datetime.date]) -> None:
        painter.save()
        with open(get_resource("config.json")) as file:
            if date.toPyDate().strftime("%Y-%m-%d") in json.loads(file.read())["favorites"]:
                painter.fillRect(rect, QtGui.QColor.fromRgb(255, 255, 0))

        pen = painter.pen()

        entry_file = EntryFile(date.toPyDate())
        if not entry_file.exists():
            painter.fillRect(rect, QtGui.QColor.fromHsl(pen.color().hue(), pen.color().saturation(), pen.color().lightness(), 50))

        if (date.month() != self.monthShown()):
            painter.setPen(QtGui.QColor("#888888"))
        elif date.dayOfWeek() == 6 or date.dayOfWeek() == 7:
            painter.setPen(QtGui.QColor("red"))

        tags = entry_file.get_tags()
        rect.adjust(0, 0, -1, -1)
        pen = painter.pen()
        pen.setColor(QtGui.QColor.fromHsl(pen.color().hue(), pen.color().saturation(), pen.color().lightness(), 150))
        if (date == QtCore.QDate.currentDate()):
            pen.setColor(QtGui.QColor.fromHsl(pen.color().hue(), pen.color().saturation(), pen.color().lightness(), 255))
            rect.adjust(2, 2, -1, -1)
            pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRect(rect)
        pen.setColor(QtGui.QColor.fromHsl(pen.color().hue(), pen.color().saturation(), pen.color().lightness(), 255))
        painter.setPen(pen)

        rect.adjust(5, 2, 0, 0)
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignTop, str(date.day()))
        rect.adjust(-5, 2, 0, 0)
        text = ""
        try:
            for tag in tags[:5]:
                if len(tag) > 12:
                    tag = str(tag[:12]) + "..."
                text += f" {tag} \n"
        except TypeError:
            text = ""
        font = QtGui.QFont()
        font.setPixelSize(10)
        painter.setFont(font)
        brush = painter.background()
        random.seed(date)
        brush.setColor(QtGui.QColor().fromHsl(randint(0, 255), randint(0, 255), randint(200, 255)))
        painter.setPen(QtGui.QColor("black"))
        painter.setBackground(brush)
        painter.setBackgroundMode(QtCore.Qt.BGMode.OpaqueMode)
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignHCenter, text)

        if entry_file.is_encrypted():
            # Draw a little lock symbol
            painter.setPen(QtGui.QColor.fromRgb(255, 130, 0))
            o = QtCore.QPoint(rect.x() + 77, rect.y() + 3)
            r = QtCore.QRect(o.x(), o.y(), 8, 8)
            painter.drawEllipse(QtCore.QPoint(o.x()+4, o.y()), 3, 3)
            painter.fillRect(r, QtGui.QColor().fromRgb(255, 130, 0))
            painter.setPen(QtGui.QColor.fromRgb(150, 50, 0))
            painter.drawLine(o.x()+4, o.y()+3, o.x()+4, o.y()+5)
        
        painter.restore()
