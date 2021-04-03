import re
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore


class EditPane(AbstractPane.AbstractPane):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.setAcceptRichText(False)
        self.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)




    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        currentCaretPosition = self.textCursor().position()
        headerPattern = re.compile("^#{1,6}[^\S\n]+.*", re.MULTILINE)
        headers = [x for x in re.finditer(headerPattern, self.toPlainText())]
        sliderPos = self.verticalScrollBar().sliderPosition()
        if len(headers) > 0:
            for header in headers:
                cursor = QtGui.QTextCursor(self.document())
                cursor.setPosition(header.start())
                cursor.setPosition(header.end(), self.textCursor().KeepAnchor)
                self.setTextCursor(cursor)
                formatter = QtGui.QTextCharFormat()
                formatter.setFontWeight(QtGui.QFont.Bold)
                cursor.mergeCharFormat(formatter)
                print(self.textCursor().position())

            formatter = QtGui.QTextCharFormat()
            formatter.setFontWeight(QtGui.QFont.Normal)
            cursor = QtGui.QTextCursor(self.document())
            cursor.setPosition(currentCaretPosition)
            cursor.mergeCharFormat(formatter)
            self.setTextCursor(cursor)
            self.verticalScrollBar().setSliderPosition(sliderPos)
            print(self.textCursor().position())
            print(self.toHtml())

        super(EditPane, self).keyReleaseEvent(e)
