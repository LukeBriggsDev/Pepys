import re

from PySide2 import QtWidgets, QtGui, QtCore


class AbstractPane(QtWidgets.QTextEdit):
    def __init__(self, ctx):
        super().__init__()
        filename = ctx.get_resource("PaneStyle.qss")
        with open(filename) as file:
            stylesheet = file.read()
        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setStyleSheet(stylesheet)
        self.setVerticalScrollBarPolicy(self.verticalScrollBarPolicy().ScrollBarAlwaysOn)


    def updateSize(self, newFrameSize):
        self.verticalScrollBar().setStyleSheet("QScrollBar:vertical {width:"+str(newFrameSize * 0.25 + 4)+";border-left-width: "+ str(newFrameSize * 0.25 - 4) +"px ;}")
        self.setStyleSheet(self.styleSheet() + "QTextEdit { border-left-width: " + str(newFrameSize * 0.25) + "px;}")


    def enterEvent(self, event:QtCore.QEvent) -> None:
        self.verticalScrollBar().setVisible(True)
        self.verticalScrollBar().setStyleSheet(self.verticalScrollBar().styleSheet() + """QScrollBar::handle:vertical {
        background-color: rgb(125,124,123);
        }""")


    def leaveEvent(self, event:QtCore.QEvent) -> None:
        self.verticalScrollBar().setVisible(False)
        self.verticalScrollBar().setStyleSheet(self.verticalScrollBar().styleSheet() + """QScrollBar::handle:vertical {
        background-color: rgb(250,249,247);
        }""")