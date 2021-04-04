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
        self.markdownHighlighter = MarkdownSyntaxHighlighter(self)



    def setCurrentFile(self, filepath: str):
        self.currentFile = filepath

    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        if(e.text() == '=' or e.text() == '-'):
            self.markdownHighlighter.rehighlightBlock(self.document().findBlock(self.textCursor().position()).previous())
