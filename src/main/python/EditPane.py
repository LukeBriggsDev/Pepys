import re
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore
from MarkdownToken import MarkdownToken
import string


class EditPane(AbstractPane.AbstractPane):


    def __init__(self, ctx):
        super().__init__(ctx)
        self.setAcceptRichText(False)
        self.currentFile = ""



    def applyFormatting(self):
        currentCaretPosition = self.textCursor().position()
        sliderPos = self.verticalScrollBar().sliderPosition()

        textPattern = re.compile("[\s\S]+?(?=[\\<!\[_*`~]|https?://| {2,}\n|$)")
        textFormatter = QtGui.QTextCharFormat()
        textFormatter.setFontItalic(False)
        textFormatter.setFontWeight(QtGui.QFont.Normal)
        textFormatter.setFontStrikeOut(False)
        textToken = MarkdownToken(textPattern, textFormatter)
        textToken.applyStyle(self)

        headerPattern = re.compile("^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)|^([^\n]+)\n *(=|-)+ *(?:\n+|$)", re.MULTILINE)
        headerFormatter = QtGui.QTextCharFormat()
        headerFormatter.setFontWeight(QtGui.QFont.Bold)
        headerToken = MarkdownToken(headerPattern, headerFormatter)
        headerToken.applyStyle(self)

        emphasisPattern = re.compile(
            r'(?<!\\)\*[^\s\*](.*?\S?.*?)(?<!\\)\*' # *this*
            r'|' # or
            r'(?<!(\\|\S))_[^\s_](.*?\S?.*?)(?<!\\)_(?=\s)' #_this_
        )
        emphasisFormatter = QtGui.QTextCharFormat()
        emphasisFormatter.setFontItalic(True)
        emphasisToken = MarkdownToken(emphasisPattern, emphasisFormatter)
        emphasisToken.applyStyle(self)

        strongEmphasisPattern = re.compile(
            r'(\*\*|__)[^\s*](.*?\S.*?)\1' # **this** or __this__
        )
        strongEmphasisFormatter = QtGui.QTextCharFormat()
        strongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
        strongEmphasisFormatter.setFontItalic(False)
        strongEmphasisToken = MarkdownToken(strongEmphasisPattern, strongEmphasisFormatter)
        strongEmphasisToken.applyStyle(self)

        veryStrongEmphasisPattern = re.compile(
            r'((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](.*?\S.*?)(?:\5\4|\3\2)' # ***this*** or ___this___
        )
        veryStrongEmphasisFormatter = QtGui.QTextCharFormat()
        veryStrongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
        veryStrongEmphasisFormatter.setFontItalic(True)
        veryStrongEmphasisToken = MarkdownToken(veryStrongEmphasisPattern, veryStrongEmphasisFormatter)
        veryStrongEmphasisToken.applyStyle(self)

        strikethroughPattern = re.compile(r"~~(?=\S)([\s\S]*?\S)~~") # ~~this~~
        strikethroughFormatter = QtGui.QTextCharFormat()
        strikethroughFormatter.setFontStrikeOut(True)
        strikethroughToken = MarkdownToken(strikethroughPattern, strikethroughFormatter)
        strikethroughToken.applyStyle(self)


        formatter = QtGui.QTextCharFormat()
        formatter.setFontWeight(QtGui.QFont.Normal)
        formatter.setFontItalic(False)
        cursor = QtGui.QTextCursor(self.document())
        #cursor.mergeCharFormat(formatter)
        cursor.setPosition(currentCaretPosition)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setSliderPosition(sliderPos)


    def setCurrentFile(self, filepath: str):
        self.currentFile = filepath

    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        allowedUpdateChars = [' ', '\n', '\r', chr(8)]
        if e.text().isalnum() or e.text() in allowedUpdateChars or e.text() in string.punctuation:
            self.applyFormatting()


        super(EditPane, self).keyReleaseEvent(e)
