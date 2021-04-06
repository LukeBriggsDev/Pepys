from PySide2 import QtWidgets, QtGui
from FileMenu import FileMenu


class CustomMenuBar(QtWidgets.QMenuBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, text_edit: QtWidgets.QTextEdit) -> None:
        super().__init__()
        file_menu = FileMenu(text_edit)
        self.setStyleSheet("background-color: rgb(250,249,247);")
        self.addMenu(file_menu)
