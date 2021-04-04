from PySide2 import QtWidgets, QtGui, QtCore
import re

class MarkdownToken:

    def __init__(self, formatter):
        self.formatter = formatter

    def applyStyle(self, textEdit: QtWidgets.QTextEdit, start, end):
        cursor = QtGui.QTextCursor(textEdit.document())
        cursor.setPosition(start)
        cursor.setPosition(end, textEdit.textCursor().KeepAnchor)
        textEdit.setTextCursor(cursor)
        cursor.mergeCharFormat(self.formatter)

