from PySide6 import QtCore, QtWidgets, QtGui


class ViewPane(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        with open("ViewPaneStyle.qss", "r") as file:
            stylesheet = file.read()

        self.setStyleSheet(stylesheet)
        self.setReadOnly(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setEnabled(False)


