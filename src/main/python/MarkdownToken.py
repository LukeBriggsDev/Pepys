from PySide2 import QtWidgets, QtGui, QtCore
import re

class MarkdownToken:

    def __init__(self, regex, formatter):
        self.regex = regex
        self.formatter = formatter

    def applyStyle(self, textEdit: QtWidgets.QTextEdit):
        matches = [x for x in re.finditer(self.regex, textEdit.toPlainText())]
        for match in matches:
            cursor = QtGui.QTextCursor(textEdit.document())
            cursor.setPosition(match.start())
            cursor.setPosition(match.end(), textEdit.textCursor().KeepAnchor)
            textEdit.setTextCursor(cursor)
            cursor.mergeCharFormat(self.formatter)

