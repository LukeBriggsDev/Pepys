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

from PyQt5 import QtWidgets, QtGui

class ActionHandler():
    """A function that stores a QAction and a function to send the action to as a parameter to when the action is triggered"""
    def __init__(self, action: QtWidgets.QAction, trigger_func):
        self.action = action
        self.action.triggered.connect(self.invoke_trigger)
        self.trigger_func = trigger_func

    def invoke_trigger(self):
        self.trigger_func(self.action)

