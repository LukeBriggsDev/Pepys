import re as regex
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore
import string
from MarkdownRegex import regexPatterns
from MarkdownSyntaxHighlighter import MarkdownSyntaxHighlighter


class EditPane(AbstractPane.AbstractPane):


    def __init__(self, ctx):
        super().__init__(ctx)
        self.setAcceptRichText(False)
        self.currentFile = ""
        self.markdownHighlighter = MarkdownSyntaxHighlighter(self.document())




    def applyFormatting(self):
        self.markdownHighlighter.highlightBlock(self.toPlainText())


    def setCurrentFile(self, filepath: str):
        self.currentFile = filepath

    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        allowedUpdateChars = [' ', chr(8)]

        if (e.text().isalnum() or e.text() in allowedUpdateChars or e.text() in string.punctuation):
            self.applyFormatting()


        super(EditPane, self).keyReleaseEvent(e)
