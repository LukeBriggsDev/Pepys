from PySide2 import QtWidgets, QtGui, QtCore
import regex
from MarkdownRegex import regexPatterns

class MarkdownSyntaxHighlighter(QtGui.QSyntaxHighlighter):

    markdownRegex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in regexPatterns)
    print(markdownRegex)
    markdownRegex = regex.compile(markdownRegex, regex.MULTILINE)


    textFormatter = QtGui.QTextCharFormat()
    textFormatter.setFontItalic(False)
    textFormatter.setFontWeight(QtGui.QFont.Normal)
    textFormatter.setFontStrikeOut(False)

    headerFormatter = QtGui.QTextCharFormat()
    headerFormatter.setFontWeight(QtGui.QFont.Bold)


    emphasisFormatter = QtGui.QTextCharFormat()
    emphasisFormatter.setFontItalic(True)

    strongEmphasisFormatter = QtGui.QTextCharFormat()
    strongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
    strongEmphasisFormatter.setFontItalic(False)


    veryStrongEmphasisFormatter = QtGui.QTextCharFormat()
    veryStrongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
    veryStrongEmphasisFormatter.setFontItalic(True)


    strikethroughFormatter = QtGui.QTextCharFormat()
    strikethroughFormatter.setFontStrikeOut(True)

    def __init__(self, textEdit:QtWidgets.QTextEdit):
        super().__init__(textEdit)

    def highlightBlock(self, text:str) -> None:
        for match in regex.finditer(self.markdownRegex, text):
            kind = match.lastgroup
            value = match.group()
            if kind == "TEXT":
                self.setFormat(match.start(), len(value), self.textFormatter)
            if kind == "HEADER":
                self.setFormat(match.start(), len(value), self.headerFormatter)
            if kind == "EMPHASIS":
                self.setFormat(match.start(), len(value), self.emphasisFormatter)
            if kind == "STRONG_EMPHASIS":
                self.setFormat(match.start(), len(value), self.strongEmphasisFormatter)
            if kind == "VERY_STRONG_EMPHASIS":
                self.setFormat(match.start(), len(value), self.veryStrongEmphasisFormatter)
            if kind == "STRIKETHROUGH":
                self.setFormat(match.start(), len(value), self.strikethroughFormatter)





