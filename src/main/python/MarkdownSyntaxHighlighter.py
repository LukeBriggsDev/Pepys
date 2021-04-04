from PySide2 import QtWidgets, QtGui, QtCore
import regex
from MarkdownRegex import regexPatterns


class MarkdownSyntaxHighlighter(QtGui.QSyntaxHighlighter):

    POSSIBLE_SETEXT_HEADER = 1


    textFormatter = QtGui.QTextCharFormat()
    textFormatter.setFontItalic(False)
    textFormatter.setFontWeight(QtGui.QFont.Normal)
    textFormatter.setFontStrikeOut(False)

    atxHeaderPattern = regex.compile(regexPatterns['ATX_HEADER'], regex.MULTILINE)
    headerFormatter = QtGui.QTextCharFormat()
    headerFormatter.setFontWeight(QtGui.QFont.Bold)

    emphasisPattern = regex.compile(regexPatterns['EMPHASIS'], regex.MULTILINE)
    emphasisFormatter = QtGui.QTextCharFormat()
    emphasisFormatter.setFontItalic(True)

    strongEmphasisPattern = regex.compile(regexPatterns['STRONG_EMPHASIS'], regex.MULTILINE)
    strongEmphasisFormatter = QtGui.QTextCharFormat()
    strongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
    strongEmphasisFormatter.setFontItalic(False)

    veryStronEmphasisPattern = regex.compile(regexPatterns['VERY_STRONG_EMPHASIS'], regex.MULTILINE)
    veryStrongEmphasisFormatter = QtGui.QTextCharFormat()
    veryStrongEmphasisFormatter.setFontWeight(QtGui.QFont.Bold)
    veryStrongEmphasisFormatter.setFontItalic(True)

    strikethroughPattern = regex.compile(regexPatterns['STRIKETHROUGH'], regex.MULTILINE)
    strikethroughFormatter = QtGui.QTextCharFormat()
    strikethroughFormatter.setFontStrikeOut(True)

    def __init__(self, textEdit:QtWidgets.QTextEdit):
        super().__init__(textEdit)

    def highlightBlock(self, text:str) -> None:

        match = regex.match(r'^([^\n]+)\n *', text)

        formatter = QtGui.QTextCharFormat()

        for match in regex.finditer(self.atxHeaderPattern, text):
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        for match in regex.finditer(self.emphasisPattern, text):
            formatter.setFontItalic(True)
            self.setFormat(match.start(), len(match.group()), formatter)

        for match in regex.finditer(self.strongEmphasisPattern, text):
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        for match in regex.finditer(self.veryStronEmphasisPattern, text):
            formatter.setFontItalic(True)
            formatter.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(match.start(), len(match.group()), formatter)

        for match in regex.finditer(self.strikethroughPattern, text):
            formatter.setFontStrikeOut(True)

            self.setFormat(match.start(), len(match.group()), formatter)




