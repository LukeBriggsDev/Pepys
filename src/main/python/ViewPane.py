from PySide2 import QtCore, QtWidgets
import AbstractPane


class ViewPane(AbstractPane.AbstractPane):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.setReadOnly(True)
        filename = ctx.get_resource("ViewPaneStyle.qss")
        with open(filename) as file:
            stylesheet = file.read()
        self.setStyleSheet(self.styleSheet() + stylesheet)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setEnabled(False)



