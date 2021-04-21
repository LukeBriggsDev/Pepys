from __future__ import annotations
import re as regex
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
    from main import AppContext


class EditPane(QtWidgets.QTextEdit):
    """ TextEdit for writing markdown text."""

    def __init__(self, ctx: AppContext) -> None:
        super().__init__()
        self.ctx = ctx
        # Set to prevent formatting being pasted from clipboard
        self.setAcceptRichText(False)
        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

        self.setVerticalScrollBarPolicy(self.verticalScrollBarPolicy().ScrollBarAlwaysOn)

        # Used to know current directory to be relative to
        self._current_file = ""
        self.markdownHighlighter = MarkdownSyntaxHighlighter(self)

    @property
    def current_file(self):
        """Returns current file path"""
        return self._current_file

    @property
    def current_file_date(self):
        """Returns current file date as list [YYYY, MM, DD]"""
        return os.path.split(self.current_file)[1][:-3]

    def set_current_file(self, filepath: typing.TextIO) -> None:
        self._current_file = filepath.name
        self.setText(filepath.read())

    def open_file_from_date(self, file_date: date):
        """Open or create a markdown file corresponding to today"""
        formatted_date = file_date.strftime("%Y-%m-%d")

        # Add ordinal to end of number if it exists
        try:
            day_of_month = num2words(file_date.day, to="ordinal_num", lang=locale.getlocale()[0])
        except NotImplementedError:
            day_of_month = file_date.day

        long_date = file_date.strftime(f"%A {day_of_month} %B %Y")

        # Get folder for today's journal entry
        config_file = self.ctx.get_resource("config.json")
        with open(config_file, "r") as file:
            file_directory = os.path.join(json.loads(file.read())["diary_directory"], str(file_date.year),
                                          str(file_date.month), formatted_date)

        # Make folder for today's entry if not already exist
        if not os.path.exists(file_directory):
            try:
                os.mkdir(file_directory)
            except FileNotFoundError:
                try:
                    os.mkdir(os.path.dirname(file_directory))
                    os.mkdir(file_directory)
                except FileNotFoundError:
                    os.mkdir(os.path.dirname(os.path.dirname(file_directory)))
                    os.mkdir(os.path.dirname(file_directory))
                    os.mkdir(file_directory)

        # Open markdown in r+ mode if it exists, else open in w+ mode
        try:
            with open(os.path.join(file_directory, f"{formatted_date}.md"), "r+") as file:
                self.set_current_file(file)

        except FileNotFoundError:
            with open(os.path.join(file_directory, f"{formatted_date}.md"), "w+") as file:
                self.set_current_file(file)
                self.setText('---\n'
                             f'title: {long_date}\n'
                             f'date: {formatted_date}\n'
                             'tags: []\n'
                             '---\n')
        self.save_current_file()
        self.parentWidget().tool_bar.favorite_button.refresh_icon()
        self.window().setWindowTitle(long_date)

        print(self.current_file)

    def save_current_file(self) -> None:
        """Save currently open file"""

        # Get folder for today's journal entry
        print(self.current_file)
        with open(self.current_file, "w+") as file:
            file.write(self.toPlainText())

    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        """"Override base QTextEdit method, called when key is released

        :param e: the QEvent that caused the invocation
        """
        # If a key entered is a markdown Setext header underline, re-highlight previous line to form full header
        current_line = self.document().findBlock(self.textCursor().position())
        if '=' in current_line.text() or '-' in current_line.text():
            self.markdownHighlighter.rehighlightBlock(
                current_line.previous())

        self.save_current_file()

    def enterEvent(self, event: QtCore.QEvent) -> None:
        """"Override base QTextEdit method, called when mouse is over TextEdit

        :param event: the QEvent that caused the invocation
        """

        self.verticalScrollBar().setVisible(True)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        """"Override base QTextEdit method, called when mouse leaves TextEdit

        :param event: the QEvent that caused the invocation
        """

        self.verticalScrollBar().setVisible(False)
