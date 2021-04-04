import regex
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore
from MarkdownToken import MarkdownToken
import string
from MarkdownRegex import regexPatterns


class EditPane(AbstractPane.AbstractPane):


    markdownRegex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in regexPatterns)


    textFormatter = QtGui.QTextCharFormat()
    textFormatter.setFontItalic(False)
    textFormatter.setFontWeight(QtGui.QFont.Normal)
    textFormatter.setFontStrikeOut(False)
    textToken = MarkdownToken(textFormatter)

    headerFormatter = QtGui.QTextCharFormat()
    headerFormatter.setFontWeight(QtGui.QFont.Bold)
    headerToken = MarkdownToken(headerFormatter)


    emphasisFormatter = QtGui.QTextCharFormat()
    emphasisFormatter.setFontItalic(True)
    emphasisToken = MarkdownToken(emphasisFormatter)

    strongEmphasisFormatter = QtGui.QTextCharFormat()
    strongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
    strongEmphasisFormatter.setFontItalic(False)
    strongEmphasisToken = MarkdownToken(strongEmphasisFormatter)


    veryStrongEmphasisFormatter = QtGui.QTextCharFormat()
    veryStrongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
    veryStrongEmphasisFormatter.setFontItalic(True)
    veryStrongEmphasisToken = MarkdownToken(veryStrongEmphasisFormatter)


    strikethroughFormatter = QtGui.QTextCharFormat()
    strikethroughFormatter.setFontStrikeOut(True)
    strikethroughToken = MarkdownToken(strikethroughFormatter)

    def __init__(self, ctx):
        super().__init__(ctx)
        self.setAcceptRichText(False)
        self.currentFile = ""




    def applyFormatting(self):

        for match in regex.finditer(self.markdownRegex, self.toPlainText()):
            kind = match.lastgroup
            value = match.group()
            if kind == "TEXT":
                self.textToken.applyStyle(self, match.start(), match.end())
            elif kind == "HEADER":
                self.headerToken.applyStyle(self, match.start(), match.end())
            elif kind == "EMPHASIS":
                self.emphasisToken.applyStyle(self, match.start(), match.end())
            elif kind == "STRONG_EMPHASIS":
                self.strongEmphasisToken.applyStyle(self, match.start(), match.end())
            elif kind == "VERY_STRONG_EMPHASIS":
                self.veryStrongEmphasisToken.applyStyle(self, match.start(), match.end())
            elif kind == "STRIKETHROUGH":
                self.strikethroughToken.applyStyle(self, match.start(), match.end())



        currentCaretPosition = self.textCursor().position()
        sliderPos = self.verticalScrollBar().sliderPosition()

        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(currentCaretPosition)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setSliderPosition(sliderPos)


    def setCurrentFile(self, filepath: str):
        self.currentFile = filepath

    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        allowedUpdateChars = [' ', '\n', '\r', chr(8)]
        allowedPunctuation = string.punctuation
        if (e.text().isalnum() or e.text() in allowedUpdateChars or e.text() in string.punctuation) and e.text() != "":
            self.applyFormatting()


        super(EditPane, self).keyReleaseEvent(e)
