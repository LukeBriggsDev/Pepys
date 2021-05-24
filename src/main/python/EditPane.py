from __future__ import annotations

import json
import locale
import os
import sys
import typing
from datetime import date
import enchant
import regex
from enchant.tokenize import get_tokenizer
import shutil
import pathlib
import CONSTANTS

from PyQt5 import QtWidgets, QtGui, QtCore
from num2words import num2words

from CONSTANTS import get_resource, spell_lang, spell_dict
from MarkdownSyntaxHighlighter import MarkdownSyntaxHighlighter
from ActionHandler import ActionHandler

if typing.TYPE_CHECKING:
    from main import AppContext


class EditPane(QtWidgets.QTextEdit):
    """ TextEdit for writing markdown text."""

    # Load tokenizer
    try:
        spell_tknzr = get_tokenizer(spell_lang)
    except enchant.errors.TokenizerNotFoundError:
        spell_tknzr = get_tokenizer()

    spell_suggestion_handlers = []
    file_changed = QtCore.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        tab_stop = 4
        self.setFontPointSize(14)
        font = QtGui.QFont()
        if sys.platform.startswith("linux"):
            font = QtGui.QFont("monospace")
        elif sys.platform.startswith("darwin"):
            font = QtGui.QFont("SF Mono")
        elif sys.platform.startswith("win"):
            font = QtGui.QFont("Consolas")
        font.setStyleHint(QtGui.QFont.Monospace)
        self.document().setDefaultFont(font)
        # Set tab width
        metrics = QtGui.QFontMetrics(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))

        self.setTabStopDistance(metrics.width(" " * tab_stop))
        # Set to prevent formatting being pasted from clipboard
        self.setAcceptRichText(False)
        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

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
        self.file_changed.emit()
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

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        super(EditPane, self).keyPressEvent(e)
        current_line = self.document().findBlock(self.textCursor().position())
        # Auto add list
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            # If the previous line started with a number list entry
            match = regex.match(r"^(?P<number>[0-9]+)(?P<sep>[\.)]+ )", current_line.previous().text())
            if match is not None:
                self.insertPlainText(str(int(match.group("number")) + 1) + match.group("sep"))

            # If the previous line started with a lettered list entry
            match = regex.match(r"^(?P<letter>[A-Ya-y]{1})(?P<sep>[\.)]+ )", current_line.previous().text())
            if match is not None:
                self.insertPlainText(chr(ord(match.group("letter")) + 1) + match.group("sep"))

            # If the previous line is a bullet
            match = regex.match(r"^([*+\-]{1}|#\.) ", current_line.previous().text())
            if match is not None:
                self.insertPlainText(match.group())




        self.save_current_file()

    def contextMenuEvent(self, e:QtGui.QContextMenuEvent) -> None:
        context_menu = self.createCustomContextMenu(e.pos())
        context_menu.exec_(e.globalPos())

    def insert_image(self):
        image_dialog = QtWidgets.QFileDialog(caption="Insert Image", directory=pathlib.Path.home().as_posix(),
                                             filter="Image Files(*.apng *.avif *.gif *.jpg *.jpeg *.jfif *.pjpeg, *.pjp *.png *.svg *.webp)")
        image_dialog.exec_()
        image = image_dialog.selectedFiles()[0]
        shutil.copy(image, pathlib.Path(self.current_file).parent)
        self.insertPlainText(f"![]({pathlib.Path(image).name})")
        self.save_current_file()

    def insert_table(self, table: list[list[str]], type: int, include_headers: bool):
        """Insert a table based off a given list of lists of text edits [row][col] and the type of table
            :param table: list of rows, each being a list of columns within the row with text as elements
            :param type: the type of table to enter.
                        0 = simple multiline table
                        1 = grid table
            :param include_headers: Whether the top row should be treated as a header
        """
        grid_table = 1
        simple_table = 0
        table_str = "\n"
        vertex_char = "+" if type == grid_table else " "
        divider_char = "|" if type == grid_table else " "

        # List of column widths
        column_widths = [0] * len(table[0])
        # Assign lengths of column widths to corresponding index
        for row in range(len(table)):
            for col in range(len(table[row])):
                if len(max(table[row][col].split("\n"), key=len)) > column_widths[col]:
                    column_widths[col] = len(max(table[row][col].split("\n"), key=len))

        # Create top bar
        if type == grid_table:
            table_str += vertex_char
            for col in range(len(table[0])):
                table_str += "-"* column_widths[col] + vertex_char
            table_str += "\n"
        else:
            table_str += "-" * (sum(column_widths) + ((len(table[0]) -1) * len(divider_char))) + vertex_char + "\n"

        # Main content
        for row in range(len(table)):
            column_text = [text for text in table[row]]
            # List of columns, each column is a list split by newline
            column_by_lines = [column.split("\n") for column in column_text]
            # Number of lines of longest column
            max_lines = len(max(column_by_lines, key=len))

            for line in range(max_lines):
                # Add divider to beginning of grid table line
                if type == grid_table:
                    table_str += divider_char

                for col in range(len(column_text)):
                    try:
                        table_str += column_by_lines[col][line]
                        # If current line is the longest in the table
                        if len(column_by_lines[col][line]) == column_widths[col]:
                            table_str += divider_char
                        else:
                            table_str += " " * (column_widths[col] - len(column_by_lines[col][line])) + divider_char
                    except IndexError:
                        table_str += " " * column_widths[col] + divider_char
                table_str += "\n"

            # Creat double dashed line on first line if headers enabled
            if row ==0 and type == grid_table and include_headers:
                table_str += vertex_char
                for col in range(len(table[0])):
                    table_str += "="* column_widths[col] + vertex_char

            # Create simple dashed line on first row (header on simple table) or at the end of each row in a grid table
            elif (row == 0 and type == simple_table and include_headers) or (type == grid_table):
                if type == grid_table:
                    table_str += vertex_char
                for col in range(len(table[0])):
                    table_str += "-"* column_widths[col] + vertex_char

            table_str += "\n"

        # Create bottom bar
        if type == simple_table:
            table_str += "-" * (sum(column_widths) + len(table[0]) -1) + "\n"

        self.insertPlainText(table_str)
        self.save_current_file()


    def createCustomContextMenu(self, pos) -> QtWidgets.QMenu:
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction(QtGui.QIcon(get_resource(CONSTANTS.icons["plus"][CONSTANTS.theme])), "Insert Image", self.insert_image)
        menu.addSeparator()
        self.word_cursor = self.cursorForPosition(pos)
        self.word_cursor.select(QtGui.QTextCursor.WordUnderCursor)
        # Find misspelled word in highlighted text
        misspelled = [token[0] for token in self.spell_tknzr(self.word_cursor.selectedText()) if token[0][0].islower() and not spell_dict.check(token[0])]

        # If there is a misspelled word and the word matches the whole of the highlighted text
        if len(misspelled) > 0 and misspelled[0] == self.word_cursor.selectedText():
            # Add 'Add to Dictionary option'
            self.add_to_dict_action_handler = ActionHandler(menu.addAction("Add to dictionary"), self.add_to_word_list)
            menu.addSeparator()

            spell_suggestion_handlers = []
            # Get spelling suggestions
            spell_suggestions = spell_dict.suggest(misspelled[0])
            # Add suggestions to menu until there is no more left or a maximum of 10
            while len(spell_suggestion_handlers) < 10 and len(spell_suggestion_handlers) < len(spell_suggestions):
                for suggestion in spell_suggestions:
                    new_action = menu.addAction(suggestion)
                    spell_suggestion_handlers.append(ActionHandler(new_action, self.replace_selection))

            # Save suggestion handlers to object so they persist
            self.spell_suggestion_handlers = spell_suggestion_handlers


            if len(self.spell_suggestion_handlers) == 0:
                no_suggestions = menu.addAction("No Suggestions")
                no_suggestions.setEnabled(False)


        return menu

    def replace_selection(self, action: QtWidgets.QAction):
        self.word_cursor.insertText(action.text())
        self.save_current_file()

    def add_to_word_list(self, action: QtWidgets.QAction):
        spell_dict.add_to_pwl(self.word_cursor.selectedText())
        self.markdownHighlighter.rehighlight()

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

    def insertFromMimeData(self, source: QtCore.QMimeData) -> None:
        if source.hasText():
            self.insertPlainText(source.text())
        else:
            super().insertFromMimeData(source)