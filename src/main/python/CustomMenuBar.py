from PySide2 import QtWidgets, QtGui
from FileMenu import FileMenu

class CustomMenuBar(QtWidgets.QMenuBar):
    def __init__(self, textEdit: QtWidgets.QTextEdit):
        super().__init__()
        fileMenu = FileMenu(textEdit)
        self.setStyleSheet("background-color: rgb(250,249,247);")
        self.addMenu(fileMenu)