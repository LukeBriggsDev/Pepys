from __future__ import annotations
import re as regex
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore
import string
from MarkdownRegex import regexPatterns
from MarkdownSyntaxHighlighter import MarkdownSyntaxHighlighter
import typing
if typing.TYPE_CHECKING:
    from AppContext import AppContext


class EditPane(AbstractPane.AbstractPane):
    """ AbstractPane for writing markdown text."""

    def __init__(self, ctx: AppContext) -> None:
        super().__init__(ctx)
        # Set to prevent formatting being pasted from clipboard
        self.setAcceptRichText(False)

        # Used to know current directory to be relative to
        self.current_file = ""
        self.markdownHighlighter = MarkdownSyntaxHighlighter(self)

    def set_current_file(self, filepath: str) -> None:
        self.current_file = filepath

    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        # If a key entered is a markdown Setext header underline, re-highlight previous line to form full header
        if e.text() == '=' or e.text() == '-':
            self.markdownHighlighter.rehighlightBlock(
                self.document().findBlock(self.textCursor().position()).previous())
