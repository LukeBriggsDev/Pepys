from __future__ import annotations

import json
import locale
import os
import typing
from datetime import date
import enchant
from enchant.tokenize import get_tokenizer

from PySide2 import QtWidgets, QtGui, QtCore
from num2words import num2words

from CONSTANTS import get_resource
from MarkdownSyntaxHighlighter import MarkdownSyntaxHighlighter
from ReplaceActionHandler import ReplaceActionHandler

if typing.TYPE_CHECKING:
    from main import AppContext


class EditPane(QtWidgets.QTextEdit):
    """ TextEdit for writing markdown text."""

    # Load system default dictionary
    spell_lang = enchant.get_default_language() if enchant.dict_exists(enchant.get_default_language()) else "en_US"
    # Load spell dictionary
    spell_dict = enchant.request_dict(spell_lang)
    # Load tokenizer
    try:
        spell_tknzr = get_tokenizer(spell_lang)
    except enchant.errors.TokenizerNotFoundError:
        spell_tknzr = get_tokenizer()

    spell_suggestion_handlers = []

    def __init__(self) -> None:
        super().__init__()
        self.setFontFamily(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont).family())
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
        config_file = get_resource("config.json")
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
        # Update view pane


    def save_current_file(self) -> None:
        """Save currently open file"""

        # Get folder for today's journal entry
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
            self.markdownHighlighter.rehighlightBlock(
                current_line.next())
        self.save_current_file()

    def contextMenuEvent(self, e:QtGui.QContextMenuEvent) -> None:
        context_menu = self.createCustomContextMenu(e.pos())
        context_menu.exec_(e.globalPos())


    def createCustomContextMenu(self, pos) -> QtWidgets.QMenu:
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        # Find misspelled word in highlighted text
        misspelled = [token[0] for token in self.spell_tknzr(self.textCursor().selectedText()) if token[0][0].islower() and not self.spell_dict.check(token[0])]

        # If there is a misspelled word and the word matches the whole of the highlighted text
        if len(misspelled) > 0 and misspelled[0] == self.textCursor().selectedText():
            spell_suggestion_handlers = []
            # Get spelling suggestions
            spell_suggestions = self.spell_dict.suggest(misspelled[0])
            # Add suggestions to menu until there is no more left or a maximum of 10
            while len(spell_suggestion_handlers) < 10 and len(spell_suggestion_handlers) < len(spell_suggestions):
                for suggestion in spell_suggestions:
                    new_action = menu.addAction(suggestion)
                    spell_suggestion_handlers.append(ReplaceActionHandler(new_action, self.replace_selection))

            # Save suggestion handlers to object so they persist
            self.spell_suggestion_handlers = spell_suggestion_handlers


            if len(self.spell_suggestion_handlers) == 0:
                no_suggestions = menu.addAction("No Suggestions")
                no_suggestions.setEnabled(False)


        return menu

    def replace_selection(self, action: QtWidgets.QAction):
        self.textCursor().insertText(action.text())
        self.save_current_file()

    def enterEvent(self, event: QtCore.QEvent) -> None:
        """"Override base QTextEdit mprint(e)ethod, called when mouse is over TextEdit

        :param event: the QEvent that caused the invocation
        """

        self.verticalScrollBar().setVisible(True)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        """"Override base QTextEdit method, called when mouse leaves TextEdit

        :param event: the QEvent that caused the invocation
        """

        self.verticalScrollBar().setVisible(False)
