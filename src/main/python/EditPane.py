"""
    Copyright (C) 2021  Luke Briggs <lukebriggs02@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

import json
import sys
import typing
from datetime import date
import enchant
import regex
from enchant.tokenize import get_tokenizer
import pathlib
import CONSTANTS

from PyQt6 import QtWidgets, QtGui, QtCore
from num2words import num2words

from CONSTANTS import get_resource, spell_lang, spell_dict
from MarkdownSyntaxHighlighter import MarkdownSyntaxHighlighter
from ActionHandler import ActionHandler
from EntryFile import EntryFile

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
        font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
        font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
        self.document().setDefaultFont(font)
        # Set tab width
        metrics = QtGui.QFontMetrics(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont))


        self.setTabStopDistance(metrics.boundingRect(" " * tab_stop).width())
        # Set to prevent formatting being pasted from clipboard
        self.setAcceptRichText(False)
        self.setWordWrapMode(QtGui.QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Used to know current directory to be relative to
        self._entry_file = EntryFile(None)
    
        self.markdownHighlighter = MarkdownSyntaxHighlighter(self)

        self.setStyleSheet("""
        QTextEdit:Focus{
            border: 0px solid white;
        }
        QTextEdit{
            border: 0px solid white;
        }
        """)

    @property
    def current_file(self):
        """Returns current file path"""
        return self._entry_file.path

    @property
    def current_file_date(self):
        """Returns current file date formatted as YYYY-MM-DD"""
        return self._entry_file.formatted_date

    def set_current_file(self, filepath: typing.TextIO) -> None:
        self._entry_file = EntryFile(filepath.name)
        self.setText(filepath.read())

    def open_file_from_date(self, file_date: date):
        """Open or create a markdown file corresponding to today"""
        self._entry_file = EntryFile(file_date)

        try:
            self._entry_file.create_directory()
        except (PermissionError, OSError):
            self.no_journal_dialog = QtWidgets.QMessageBox()
            self.no_journal_dialog.setText("You do not have permission to put a diary here")
            self.no_journal_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Close |
                                                      QtWidgets.QMessageBox.StandardButton.Open)
            self.no_journal_dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Open)
            answer = self.no_journal_dialog.exec()
            if answer == QtWidgets.QMessageBox.StandardButton.Open:
                self.parent().select_diary_directory()
            else:
                exit(0)
            return

        if self._entry_file.exists():
            self.setText(self._entry_file.get_content())
        else:
            self.setText(self._entry_file.get_header_text())
       
        self.file_changed.emit()
        self.window().setWindowTitle(self._entry_file.long_date)
        self.set_margins()
        # Set font size
        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            try:
                self.parent().tool_bar.font_spinbox.setValue(config_dict["font_size"])
            except KeyError:
                # Font size not in config
                self.parent().tool_bar.font_spinbox.setValue(int(self.fontPointSize()))

        self.parent().tool_bar.entry_file_changed()
        
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
        if e.key() == QtCore.Qt.Key.Key_Enter or e.key() == QtCore.Qt.Key.Key_Return:
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

    def contextMenuEvent(self, e:QtGui.QContextMenuEvent) -> None:
        context_menu = self.createCustomContextMenu(e.pos())
        # Fix white border in context menu in Windows dark mode
        context_menu.setStyleSheet(""
                            "QMenu{background-color: palette(window);}"
                            "QMenu::item:selected{background-color: palette(highlight);}")
        context_menu.exec(e.globalPos())

    def insert_image(self):
        image_dialog = QtWidgets.QFileDialog(caption="Insert Image", directory=pathlib.Path.home().as_posix(),
                                             filter="Image Files(*.apng *.avif *.gif *.jpg *.jpeg *.jfif *.pjpeg, *.pjp *.png *.svg *.webp)")
        if image_dialog.exec() == 1:
            image = image_dialog.selectedFiles()[0]
            relative_path = self._entry_file.copy_image(image)
            self.insertPlainText(f"![]({relative_path})")

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


    def createCustomContextMenu(self, pos) -> QtWidgets.QMenu:
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        add_icon = QtGui.QIcon(get_resource(CONSTANTS.icons["plus"][CONSTANTS.theme]))
        if sys.platform != "win32": # Don't add plus icon on windows (looks ugly)
            menu.addAction(add_icon, "Insert Image", self.insert_image)
        else:
            menu.addAction("Insert Image", self.insert_image)
        menu.addSeparator()
        self.word_cursor = self.cursorForPosition(pos)
        self.word_cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
        enable_dict = False
        with open(CONSTANTS.get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
            enable_dict = config_dict["enable_dict"]
        if enable_dict:
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

    def replace_selection(self, action: QtGui.QAction):
        self.word_cursor.insertText(action.text())

    def add_to_word_list(self, action: QtGui.QAction):
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
        super().leaveEvent(event)
        self._entry_file.save(self.toPlainText())
        self.verticalScrollBar().setVisible(False)

    def insertFromMimeData(self, source: QtCore.QMimeData) -> None:
        if source.hasText():
            self.insertPlainText(source.text())
        else:
            super().insertFromMimeData(source)

    def set_margins(self):
        margin_size = max(0, int((self.window().width() - 1000) * 0.5))
        top_margin_size = max(0, int((self.window().width() - 1000) * 0.1))

        format = self.document().rootFrame().frameFormat()
        format.setBottomMargin(100)
        format.setTopMargin(top_margin_size)
        format.setLeftMargin(margin_size)
        format.setRightMargin(margin_size)
        self.document().rootFrame().frameFormat().setRightMargin(margin_size)
        self.document().rootFrame().setFrameFormat(format)
