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
import json
import re
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
import CONSTANTS

def text_to_rgb(color: str) -> QColor:
    """Takes a colour as a string in the form 'rgb(r, g, b)' and returns a QColor"""
    levels_str = color[4: -1].split(',')
    levels = [int(x) for x in levels_str]
    return QColor(levels[0], levels[1], levels[2])

def parse_stylesheet(stylesheet_file_path: str, theme: str) -> str:
    """Parses stylesheet files with logical formatting to a readable form
    :param stylesheet_file_path: path to the stylesheet file to parse
    :param theme: theme to convert colors to
    :return stylesheet as a string
    """
    palette = QtWidgets.QApplication.palette()
    palette_map = {
        "WindowText": palette.ColorRole.WindowText,
        "Button": palette.ColorRole.Button,
        "Light": palette.ColorRole.Light,
        "Midlight": palette.ColorRole.Midlight,
        "Dark": palette.ColorRole.Dark,
        "Mid": palette.ColorRole.Mid,
        "Text": palette.ColorRole.Text,
        "BrightText": palette.ColorRole.BrightText,
        "ButtonText": palette.ColorRole.ButtonText,
        "Base": palette.ColorRole.Base,
        "Window": palette.ColorRole.Window,
        "Shadow": palette.ColorRole.Shadow,
        "Highlight": palette.ColorRole.Highlight,
        "HighlightedText": palette.ColorRole.HighlightedText,
        "Link": palette.ColorRole.Link,
        "LinkVisited": palette.ColorRole.LinkVisited,
        "AlternateBase": palette.ColorRole.AlternateBase,
        "NoRole": palette.ColorRole.NoRole,
        "ToolTipBase": palette.ColorRole.ToolTipBase,
        "ToolTipText": palette.ColorRole.ToolTipText,
    }
    with open(stylesheet_file_path, "r") as pane_style:
        stylesheet = pane_style.read()
        for color_role in palette_map.keys():
            stylesheet = re.sub(f"%{color_role}%", palette.color(palette_map[color_role]).name(), stylesheet)

    return stylesheet
