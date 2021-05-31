from __future__ import annotations

import typing

import pypandoc
from PySide2 import QtGui, QtCore, QtWebEngineWidgets, QtWidgets

import CONSTANTS
from CONSTANTS import get_resource
from ColorParser import parse_stylesheet
from EditPane import EditPane

if typing.TYPE_CHECKING:
    pass

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
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def open_in_browser(self, url:QtCore.QUrl) -> None:
        """Open links in browser
        :param url: Url of file
        """
        if url.path()[-3:] != ".md":

            self.back()
            QtGui.QDesktopServices.openUrl(url)

    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change background colour when style changes to match themeZ
        if event.type() == QtCore.QEvent.StyleChange:
            self.page().setBackgroundColor(QtWidgets.QApplication.palette().color(QtGui.QPalette.Base))

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



