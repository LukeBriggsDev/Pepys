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
        sliderPos = self.verticalScrollBar().sliderPosition()

        textPattern = re.compile("[\s\S]+?(?=[\\<!\[_*`~]|https?://| {2,}\n|$)")

        headerPattern = re.compile("^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)", re.MULTILINE)
        emphasisPattern =     emphasis = re.compile(
            r'^\b_((?:__|[^_])+?)_\b'  # _this_
            r'|'
            r'^\*((?:\*\*|[^\*])+?)\*(?!\*)'  # *this*
        )

        text = [x for x in re.finditer(textPattern, self.toPlainText())]
        for match in text:
            cursor = QtGui.QTextCursor(self.document())
            cursor.setPosition(match.start())
            cursor.setPosition(match.end(), self.textCursor().KeepAnchor)
            self.setTextCursor(cursor)
            formatter = QtGui.QTextCharFormat()
            formatter.setFontWeight(QtGui.QFont.Normal)
            formatter.setFontItalic(False)
            cursor.mergeCharFormat(formatter)


        headers = [x for x in re.finditer(headerPattern, self.toPlainText())]
        print("WOO")
        for header in headers:
            cursor = QtGui.QTextCursor(self.document())
            cursor.setPosition(header.start())
            cursor.setPosition(header.end(), self.textCursor().KeepAnchor)
            self.setTextCursor(cursor)
            formatter = QtGui.QTextCharFormat()
            formatter.setFontWeight(QtGui.QFont.Bold)
            cursor.mergeCharFormat(formatter)

        emphasis = [x for x in re.finditer(emphasisPattern, self.toPlainText())]

        for emphasis in emphasis:
            cursor = QtGui.QTextCursor(self.document())
            cursor.setPosition(emphasis.start())
            cursor.setPosition(emphasis.end(), self.textCursor().KeepAnchor)
            self.setTextCursor(cursor)
            formatter = QtGui.QTextCharFormat()
            formatter.setFontItalic(True)
            cursor.mergeCharFormat(formatter)

        formatter = QtGui.QTextCharFormat()
        formatter.setFontWeight(QtGui.QFont.Normal)
        formatter.setFontItalic(False)
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(currentCaretPosition)
        cursor.mergeCharFormat(formatter)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setSliderPosition(sliderPos)


    def setCurrentFile(self, filepath: str):
        self.currentFile = filepath

    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        allowedUpdateChars = [' ', '\n', '\r', chr(8)]
        if e.text().isalnum() or e.text() in allowedUpdateChars:
            self.applyFormatting()


        super(EditPane, self).keyReleaseEvent(e)
