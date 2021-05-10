from __future__ import annotations

import typing

import pypandoc
from PySide2 import QtWidgets, QtGui, QtCore

from CONSTANTS import get_resource
import CONSTANTS
from ColorParser import *

if typing.TYPE_CHECKING:
    from EditPane import EditPane
    from WebView import WebView

class PreviewButton(QtWidgets.QPushButton):
    """Button for showing html preview"""
    def __init__(self, edit_pane: EditPane, web_view: WebView):
        """Constructor
        :param edit_pane: EditPane containing markdown to be converted
        :param web_view: WebView where the preview will be shown
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.view_pane = web_view
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(get_resource("icons/book.svg")))
        self.setToolTip("Preview")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.edit_pane.setVisible(not self.edit_pane.isVisible())
        self.refresh_page()

        if self.view_pane.isVisible():
            self.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview"][CONSTANTS.theme])))
        else:
            self.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview_stop"][CONSTANTS.theme])))
        self.view_pane.setVisible(not self.view_pane.isVisible())


    def refresh_icon(self) -> None:
        """Function for refreshing icon to match theme"""
        if not self.view_pane.isVisible():
            self.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview"][CONSTANTS.theme])))
        else:
            self.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview_stop"][CONSTANTS.theme])))

    def refresh_page(self) -> None:
        """Convert markdown to html and set webView"""
        parsed_stylesheet = parse_stylesheet(get_resource('ViewPaneStyle.css'),
                                             get_resource('colors.json'),
                                             get_resource('config.json'))

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

        self.view_pane.setHtml(html, QtCore.QUrl().fromLocalFile(self.edit_pane.current_file))
