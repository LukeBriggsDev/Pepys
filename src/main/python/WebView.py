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

import sys
import typing

from PyQt6 import QtGui, QtCore, QtWebEngineWidgets, QtWidgets
import CONSTANTS
from CONSTANTS import get_resource
import pypandoc
from EditPane import EditPane
from ColorParser import parse_stylesheet
import pathlib
import os

if typing.TYPE_CHECKING:
    from main import AppContext

class WebView(QtWebEngineWidgets.QWebEngineView):
    """WebEngineView for showing rendered markdown"""
    def __init__(self, edit_pane: EditPane):
        """Constructor
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.setVisible(False)
        # Font settings

        self.bg_colors = {'light': QtGui.QColor(255, 255, 255), 'dark': QtGui.QColor(41, 41, 41)}

        self.urlChanged.connect(self.open_in_browser)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def open_in_browser(self, url:QtCore.QUrl) -> None:
        """Open links in browser
        :param url: Url of file
        """
        if url.path()[-3:] != ".md":

            self.back()
            QtGui.QDesktopServices.openUrl(url)

    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change background colour when style changes to match themeZ
        if event.type() == QtCore.QEvent.Type.StyleChange:
            self.page().setBackgroundColor(QtWidgets.QApplication.palette().color(QtGui.QPalette.ColorRole.Base))

    def refresh_page(self):
        """Convert markdown to html and set webView"""
        parsed_stylesheet = parse_stylesheet(get_resource('ViewPaneStyle.css'), CONSTANTS.theme)

        # Write parsed stylesheet to file so it can be passed to pandoc
        with open(get_resource("parsed_stylesheet.css"), "w") as file:
            file.write(parsed_stylesheet)

        # Convert markdown to html using pandoc
        html = pypandoc.convert_text(self.edit_pane.toPlainText(), "html", format="markdown",extra_args=[
            f"--highlight-style={get_resource('syntax.theme')}",
            "-s",
            "--css="
            f"{get_resource('parsed_stylesheet.css')}",
            f"--katex={get_resource('katex/')}"
        ])
        self.setHtml(html, QtCore.QUrl().fromLocalFile(self.edit_pane.current_file))



