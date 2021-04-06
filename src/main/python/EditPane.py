from __future__ import annotations
import re as regex
import AbstractPane
from PySide2 import QtWidgets, QtGui, QtCore
import string
from MarkdownRegex import regexPatterns
from MarkdownSyntaxHighlighter import MarkdownSyntaxHighlighter
import typing
from datetime import date
import json
import os
from num2words import num2words
import locale
if typing.TYPE_CHECKING:
    from AppContext import AppContext


class EditPane(AbstractPane.AbstractPane):
    """ AbstractPane for writing markdown text."""

    def __init__(self, ctx: AppContext) -> None:
        super().__init__(ctx)
        self.ctx = ctx
        # Set to prevent formatting being pasted from clipboard
        self.setAcceptRichText(False)

        # Used to know current directory to be relative to
        self._current_file = ""
        self.markdownHighlighter = MarkdownSyntaxHighlighter(self)

    def set_current_file(self, filepath: typing.TextIO) -> None:
        self._current_file = filepath.name
        self.setText(filepath.read())

    def open_file_from_date(self, file_date: date):
        """Open or create a markdown file corresponding to today"""
        formatted_date = file_date.strftime("%Y-%m-%d")

        # Get folder for today's journal entry
        config_file = self.ctx.get_resource("config.json")
        with open(config_file, "r") as file:
            file_directory = os.path.join(json.loads(file.read())["diary_directory"], formatted_date)

        # Make folder for today's entry if not already exist
        if not os.path.exists(file_directory):
            os.mkdir(file_directory)

        # Open markdown in r+ mode if it exists, else open in w+ mode
        try:
            with open(os.path.join(file_directory, f"{formatted_date}.md"), "r+") as file:
                self.set_current_file(file)

        except FileNotFoundError:
            with open(os.path.join(file_directory, f"{formatted_date}.md"), "w+") as file:
                self.set_current_file(file)

        try:
            day_of_month = num2words(file_date.day, to="ordinal_num", lang=locale.getlocale(locale.LC_TIME)[0])
            print(day_of_month)
        except NotImplementedError:
            day_of_month = file_date.day

        self.window().setWindowTitle(file_date.strftime(f"%A {day_of_month} %B %Y"))

        print(self.current_file)

    def save_current_file(self):
        """Save currently open file"""

        # Get folder for today's journal entry
        print(self.current_file)
        with open(self.current_file, "r+") as file:
            file.write(self.toPlainText())


    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        # If a key entered is a markdown Setext header underline, re-highlight previous line to form full header
        if e.text() == '=' or e.text() == '-':
            self.markdownHighlighter.rehighlightBlock(
                self.document().findBlock(self.textCursor().position()).previous())

    @property
    def current_file(self):
        return self._current_file
