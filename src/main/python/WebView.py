from PySide2 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets

class WebView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
