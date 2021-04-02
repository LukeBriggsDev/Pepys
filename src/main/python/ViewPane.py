from PySide2 import QtCore, QtWidgets, QtGui
import os

class ViewPane(QtWidgets.QTextEdit):
    def __init__(self, ctx):
        super().__init__()
        filename = ctx.get_resource("ViewPaneStyle.qss")
        with open(filename, "r") as file:
            stylesheet = file.read()

        self.setStyleSheet(stylesheet)
        self.setReadOnly(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setEnabled(False)


