from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
import pypandoc
import regex
import HTMLRenderer
import os
import json
from CalendarFileSelector import CalendarFileSelector
from ColorParser import *
if typing.TYPE_CHECKING:
    from main import AppContext
    from EditPane import EditPane
    from WebView import WebView

class PreviewButton(QtWidgets.QPushButton):
    def __init__(self, edit_pane: EditPane, web_view: WebView, ctx: AppContext):
        super().__init__()
        self.edit_pane = edit_pane
        self.view_pane = web_view
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/book.svg")))
        self.setToolTip("Preview")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.edit_pane.setVisible(not self.edit_pane.isVisible())

        self.refresh_page()

        if self.view_pane.isVisible():
            self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["preview"][self.ctx.theme])))
        else:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["preview_stop"][self.ctx.theme])))
        self.view_pane.setVisible(not self.view_pane.isVisible())


    def refresh_icon(self):
        if not self.view_pane.isVisible():
            self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["preview"][self.ctx.theme])))
        else:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["preview_stop"][self.ctx.theme])))

    def refresh_page(self):
        parsed_stylesheet = parse_stylesheet(self.ctx.get_resource('ViewPaneStyle.css'), self.ctx.get_resource('colors.json'), self.ctx.get_resource('config.json'))
        with open(self.ctx.get_resource("parsed_stylesheet.css"), "w") as file:
            file.write(parsed_stylesheet)

        html = pypandoc.convert_text(self.edit_pane.toPlainText(), "html", format="markdown",extra_args=[
            f"--highlight-style={self.ctx.get_resource('syntax.theme')}",
            "-s",
            "--include-in-header="
            f"{self.ctx.get_resource('parsed_stylesheet.css')}"
        ])

        print(html)

        self.view_pane.setHtml(html, QtCore.QUrl().fromLocalFile(self.edit_pane.current_file))
