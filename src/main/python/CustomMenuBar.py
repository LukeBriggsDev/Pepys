from PySide2 import QtWidgets, QtGui

class CustomMenuBar(QtWidgets.QMenuBar):
    def __init__(self):
        super().__init__()
        fileMenu = QtWidgets.QMenu("File")
        self.setStyleSheet("background-color: rgb(250,249,247);")
        self.addMenu(fileMenu)