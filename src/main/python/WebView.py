from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
import json
import typing
if typing.TYPE_CHECKING:
    from main import AppContext

class WebView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self.ctx = ctx
        self.setVisible(False)
        self.settings().setFontFamily(self.settings().SansSerifFont,"Inter")
        self.settings().setFontFamily(self.settings().FixedFont, "Roboto Mono")
        self.settings().setFontSize(self.settings().MinimumFontSize, 18)
        self.settings()
        self.bg_colors = {'light': QtGui.QColor(255, 255, 255), 'dark': QtGui.QColor(41, 41, 41)}
        self.urlChanged.connect(self.open_in_browser)

    def open_in_browser(self, url:QtCore.QUrl):
        if not url.isLocalFile():
            self.back()
            QtGui.QDesktopServices.openUrl(url)

    def changeEvent(self, event:QtCore.QEvent) -> None:
        if event.type() is QtCore.QEvent.Type.StyleChange:
            self.page().setBackgroundColor(self.bg_colors[self.ctx.theme])



