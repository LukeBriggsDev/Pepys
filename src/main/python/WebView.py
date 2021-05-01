from __future__ import annotations

import typing

from PySide2 import QtGui, QtCore, QtWebEngineWidgets
import CONSTANTS
from EditPane import EditPane

if typing.TYPE_CHECKING:
    from main import AppContext

class WebView(QtWebEngineWidgets.QWebEngineView):
    """WebEngineView for showing rendered markdown"""
    def __init__(self, edit_pane:EditPane):
        """Constructor
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.setVisible(False)
        # Font settings
        self.settings().setFontFamily(self.settings().SansSerifFont, QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.GeneralFont).family())
        self.settings().setFontFamily(self.settings().FixedFont, QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont).family())
        self.settings().setFontSize(self.settings().MinimumFontSize, 18)

        self.bg_colors = {'light': QtGui.QColor(255, 255, 255), 'dark': QtGui.QColor(41, 41, 41)}

        self.urlChanged.connect(self.open_in_browser)

    def open_in_browser(self, url:QtCore.QUrl) -> None:
        """Open links in browser
        :param url: Url of file
        """
        if not url.path()==self.edit_pane.current_file:

            self.back()
            QtGui.QDesktopServices.openUrl(url)

    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change background colour when style changes to match themeZ
        if event.type() is QtCore.QEvent.Type.StyleChange:
            self.page().setBackgroundColor(self.bg_colors[CONSTANTS.theme])



