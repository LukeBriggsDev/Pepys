from PySide6 import QtCore, QtWidgets, QtGui
import re


class EditPane(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        with open("EditPaneStyle.qss") as file:
            stylesheet = file.read()
        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setStyleSheet(stylesheet)
        self.setAcceptRichText(False)
        self.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)


    def keyReleaseEvent(self, e:QtGui.QKeyEvent) -> None:
        currentCaretPosition = self.textCursor().position()
        headerPattern = re.compile("^#{1,6}[^\S\n]+.*", re.MULTILINE)
        headers = [x for x in re.finditer(headerPattern, self.toPlainText())]
        if len(headers) > 0:
            print(headers)
            print(currentCaretPosition)
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
            print(self.textCursor().position())
            print(self.toHtml())

        #super(EditPane, self).keyReleaseEvent(e)

