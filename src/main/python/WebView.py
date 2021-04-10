from PySide2 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets

class WebView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.settings().setFontFamily(self.settings().SansSerifFont,"Inter")
        self.settings().setFontFamily(self.settings().FixedFont, "Roboto Mono")
        self.settings().setFontSize(self.settings().MinimumFontSize, 18)
