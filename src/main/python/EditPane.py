import re
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore


class EditPane(AbstractPane.AbstractPane):


    def __init__(self, ctx):
        super().__init__(ctx)
        self.setAcceptRichText(False)
        self.currentFile = ""



    def applyFormatting(self):
        currentCaretPosition = self.textCursor().position()
        headerPattern = re.compile("^#{1,6}[^\S\n]+.*", re.MULTILINE)
        headers = [x for x in re.finditer(headerPattern, self.toPlainText())]
        sliderPos = self.verticalScrollBar().sliderPosition()
        print("WOO")
        for header in headers:
            cursor = QtGui.QTextCursor(self.document())
            cursor.setPosition(header.start())
            cursor.setPosition(header.end(), self.textCursor().KeepAnchor)
            self.setTextCursor(cursor)
            formatter = QtGui.QTextCharFormat()
            formatter.setFontWeight(QtGui.QFont.Bold)
            cursor.mergeCharFormat(formatter)

        formatter = QtGui.QTextCharFormat()
        formatter.setFontWeight(QtGui.QFont.Normal)
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(currentCaretPosition)
        cursor.mergeCharFormat(formatter)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setSliderPosition(sliderPos)


    def setCurrentFile(self, filepath: str):
        self.currentFile = filepath

    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        allowedUpdateChars = [' ', '\n', '\r']
        if e.text().isalnum() or e.text() in allowedUpdateChars:
            self.applyFormatting()


        super(EditPane, self).keyReleaseEvent(e)
