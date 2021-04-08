from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
import mistune
import regex
import CodeSyntaxHighlighter
import os
import json
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext
    from EditPane import EditPane
    from ViewPane import ViewPane

class PreviewButton(QtWidgets.QPushButton):
    def __init__(self, edit_pane: EditPane, view_pane: ViewPane, ctx: AppContext):
        super().__init__()
        self.edit_pane = edit_pane
        self.view_pane = view_pane
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/book.svg")))
        self.setToolTip("Preview")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.edit_pane.setVisible(not self.edit_pane.isVisible())
        self.edit_pane.update_size(self.window().width())
        self.view_pane.update_size(self.window().width())

        self.view_pane.setHtml(
            mistune.markdown(self.edit_pane.toPlainText(), renderer=CodeSyntaxHighlighter.HighlightRenderer()))
        html = self.view_pane.toHtml().replace("<img ", f'<img width="{self.view_pane.width() * 0.5}" ')
        file_path_pattern = regex.compile('(?<=src=")\S*(?=")')
        filepaths = [filepath.group() for filepath in regex.finditer(file_path_pattern, self.view_pane.toHtml())]

        for filepath in filepaths:
            if filepath[0] != "/" or filepath[1] != ":":

                print(self.edit_pane.current_file)
                print(filepath)
                html = html.replace(filepath, os.path.join(os.path.dirname(self.edit_pane.current_file), filepath))

                print(html)

        self.view_pane.setHtml(html)
        if self.view_pane.isVisible():
            self.setIcon(QtGui.QIcon(self.ctx.get_resource("icons/book.svg")))
        else:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource("icons/book-fill.svg")))
        self.view_pane.setVisible(not self.view_pane.isVisible())