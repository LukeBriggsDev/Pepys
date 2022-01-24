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

import sys
import typing

from PyQt6 import QtWidgets, QtGui, QtCore

from WebView import WebView
from EntryExplorer import EntryExplorer
import json
import pathlib
import shutil

from ColorParser import parse_stylesheet

if typing.TYPE_CHECKING:
    pass

from Crypto import Crypto
from EditPane import EditPane
from EntryFile import EntryFile
from ExportWindow import ExportWindow
from TableWindow import TableWindow
from SettingsWindow import SettingsWindow
from CONSTANTS import get_resource
from CalendarFileSelector import CalendarFileSelector
import CONSTANTS

class CustomToolbar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, parent, edit_pane: EditPane, web_view: WebView) -> None:
        """Constructor
        :param edit_pane: EditPane holding currently editing document
        :param web_view: WebView to hold the output of the edit pane
        """

        super().__init__()

        self.edit_pane = edit_pane
        self.edit_pane.file_changed.connect(self.refresh_favorite)

        self.web_view = web_view

        # Calendar button
        self.open_entry_button = QtWidgets.QPushButton()
        self.open_entry_button.setMinimumSize(32, 32)
        self.open_entry_button.setMaximumSize(32, 32)
        self.open_entry_button.setToolTip("Open Entry")
        self.open_entry_button.setWhatsThis("Click this to select an entry via a calendar")
        self.open_entry_button.setIcon(QtGui.QIcon(get_resource("icons/calendar.svg")))
        self.open_entry_button.clicked.connect(self.open_entry_clicked)

        # Favorite button
        self.favorite_button = QtWidgets.QPushButton()
        self.favorite_button.setMinimumSize(32, 32)
        self.favorite_button.setMaximumSize(32, 32)
        self.refresh_favorite()
        self.setToolTip("Favourite")
        self.favorite_button.clicked.connect(self.favorite_clicked)

        # Changedir button
        self.changedir_button = QtWidgets.QPushButton()
        self.changedir_button.setMinimumSize(32, 32)
        self.changedir_button.setMaximumSize(32, 32)
        self.changedir_button.setIcon(QtGui.QIcon(get_resource("icons/folder.svg")))
        self.changedir_button.setToolTip("Change Directory")
        self.changedir_button.clicked.connect(parent.select_diary_directory)

        # Preview button
        self.preview_button = QtWidgets.QPushButton()
        self.preview_button.setMinimumSize(32, 32)
        self.preview_button.setMaximumSize(32, 32)
        self.preview_button.setIcon(QtGui.QIcon(get_resource("icons/book.svg")))
        self.preview_button.setToolTip("Preview")
        self.preview_button.clicked.connect(self.preview_clicked)

        # Font Size
        self.font_spinbox = QtWidgets.QSpinBox()
        self.font_spinbox.setMaximumSize(64, 28)
        self.font_spinbox.setMinimumSize(64, 28)
        self.font_spinbox.setToolTip("Font size")
        self.font_spinbox.setMaximum(120)
        self.font_spinbox.setMinimum(1)
        self.font_spinbox.valueChanged.connect(self.font_change)

        # Export Button
        self.export_button = QtWidgets.QPushButton()
        self.export_button.setMinimumSize(32, 32)
        self.export_button.setMaximumSize(32, 32)
        self.export_button.setIcon(QtGui.QIcon(get_resource("icons/export.svg")))
        self.export_button.setToolTip("Export")
        self.export_button.clicked.connect(self.export_clicked)

        # Insert button
        self.insert_button = QtWidgets.QPushButton()
        self.insert_button.setMinimumSize(32, 32)
        self.insert_button.setMaximumSize(32, 32)
        self.insert_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["plus"][CONSTANTS.theme])))
        self.insert_button.setToolTip("Insert")
        self.insert_button.clicked.connect(self.insert_clicked)

        # Settings button
        self.settings_button = QtWidgets.QPushButton()
        self.settings_button.setMaximumSize(32, 32)
        self.settings_button.setMinimumSize(32, 32)
        self.settings_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["settings"][CONSTANTS.theme])))
        self.settings_button.setToolTip("Settings")
        self.settings_button.clicked.connect(self.settings_clicked)

        # Theme switch button
        self.theme_switch_button = QtWidgets.QPushButton()
        self.theme_switch_button.setMinimumSize(32, 32)
        self.theme_switch_button.setMaximumSize(32, 32)
        self.theme_switch_button.setToolTip("Change theme")
        self.theme_switch_button.clicked.connect(self.theme_switch_clicked)

         # Encryption switch button
        self.encryption_switch_button = QtWidgets.QPushButton()
        self.encryption_switch_button.setMinimumSize(32, 32)
        self.encryption_switch_button.setMaximumSize(32, 32)
        self.encryption_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["unencrypted"][CONSTANTS.theme])))
        self.encryption_switch_button.setToolTip("Change encryption")
        self.encryption_switch_button.clicked.connect(self.encryption_switch_clicked)

        #Read current theme

        # Add buttons to layout
        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        self.addWidget(self.encryption_switch_button)
        self.addWidget(self.changedir_button)
        self.addWidget(self.export_button)
        self.font_label = QtWidgets.QLabel("Font size: ")
        self.font_label.setToolTip("Font size")
        self.addWidget(self.font_label)
        self.addWidget(self.font_spinbox)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.theme_switch_button)
        self.addWidget(self.insert_button)
        self.addWidget(self.preview_button)
        self.addWidget(self.settings_button)
        self.refresh_stylesheet()
        self.refesh_encryption_switch_button()

    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change button icons to match theme
        if event.type() == QtCore.QEvent.Type.PaletteChange:
            self.open_entry_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["open_entry"][CONSTANTS.theme])))
            self.refresh_favorite()

            # Refresh preview icon
            if not self.web_view.isVisible():
                self.preview_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview"][CONSTANTS.theme])))
            else:
                self.preview_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview_stop"][CONSTANTS.theme])))
            self.insert_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["plus"][CONSTANTS.theme])))
            self.theme_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["theme_switch"][CONSTANTS.theme])))
            self.export_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["export"][CONSTANTS.theme])))
            self.changedir_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["folder"][CONSTANTS.theme])))
            self.settings_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["settings"][CONSTANTS.theme])))
            if sys.platform == "win32":
                self.font_spinbox.setStyleSheet("color: black;")
            self.refesh_encryption_switch_button()

    def font_change(self, i):
        # Change font
        self.edit_pane.selectAll()
        self.edit_pane.setFontPointSize(i)
        self.edit_pane.setFocus()
        self.edit_pane.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.edit_pane.clearFocus()
        self.font_spinbox.setFocus()

        # Set size in config file
        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            config_dict["font_size"] = i

            # Write changes and refresh icon
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()

    def entry_file_changed(self):
       self.refesh_encryption_switch_button()


    def open_entry_clicked(self):
        """Open calendar dialog and disable main window"""
        self.date_dialog = CalendarFileSelector(self.edit_pane, self.web_view)
        self.setEnabled(False)
        self.date_dialog.show()

    def favorite_clicked(self):
        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            # Currently in favorites list
            if self.edit_pane.current_file_date in config_dict["favorites"]:
                # Remove from favorites
                config_dict["favorites"].remove(self.edit_pane.current_file_date)
            else:
                # Add to favorites
                config_dict["favorites"].append(self.edit_pane.current_file_date)

            # Write changes and refresh icon
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()
            self.refresh_favorite()

    def refresh_favorite(self):
        with open(get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
        if self.edit_pane.current_file_date in config_dict["favorites"]:
            self.favorite_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["favorite_on"][CONSTANTS.theme])))
        else:
            self.favorite_button.setIcon(QtGui.QIcon(get_resource((CONSTANTS.icons["favorite_off"][CONSTANTS.theme]))))

    def preview_clicked(self):
        self.edit_pane.setVisible(not self.edit_pane.isVisible())
        self.web_view.refresh_page()

        if self.web_view.isVisible():
            self.preview_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview"][CONSTANTS.theme])))
        else:
            self.preview_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview_stop"][CONSTANTS.theme])))
        self.web_view.setVisible(not self.web_view.isVisible())

    def insert_clicked(self):
        self.insert_menu = QtWidgets.QMenu()
        self.insert_menu.setStyleSheet(""
                                       "QMenu{background-color: palette(window);}"
                                       "QMenu::item:selected{background-color: palette(highlight);}")
        self.insert_menu.addAction("Insert image", self.edit_pane.insert_image)
        self.insert_menu.addAction("Insert table", self.open_table_options)
        self.insert_menu.popup(self.mapToGlobal(self.insert_button.pos() + QtCore.QPoint(- self.insert_button.width(), self.insert_button.height())))
        pass

    def open_table_options(self):
        self.table_option_dialog = TableWindow()
        insert_button = QtWidgets.QPushButton("Create Table")
        insert_button.clicked.connect(self.table_handler)
        self.table_option_dialog.layout().addWidget(insert_button)
        self.table_option_dialog.exec()

    def table_handler(self):
        table = self.table_option_dialog.table_widget
        row_list = []
        for row in range(table.rowCount()):
            col_list = []
            for col in range(table.columnCount()):
                try:
                    col_list.append(table.item(row, col).text())
                except AttributeError:
                    # Empty Cell
                    col_list.append(" ")
            row_list.append(col_list)
        self.edit_pane.insert_table(row_list,
                                    self.table_option_dialog.table_type.currentIndex(),
                                    self.table_option_dialog.include_headers.isChecked())
        self.table_option_dialog.close()

    def theme_switch_clicked(self):
        current_theme = CONSTANTS.theme

        if current_theme == "light":
            QtWidgets.QApplication.setPalette(CONSTANTS.Colors.getDarkpalette())
            CONSTANTS.theme = "dark"
        elif CONSTANTS.light_palette.color(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base).lightness() > 122:
            QtWidgets.QApplication.setPalette(CONSTANTS.light_palette)
            CONSTANTS.theme = "light"

        self.refresh_stylesheet()
        main_window = self.parentWidget()
        main_window.refresh_stylesheet()

        # Refresh web_view
        self.web_view.refresh_page()
        # Refresh edit pane
        self.edit_pane.markdownHighlighter.rehighlight()
        # Call resize event to cause update
        QtCore.QCoreApplication.postEvent(main_window, QtGui.QResizeEvent(main_window.size(), main_window.size()))

    def export_clicked(self):
        self.export_window = ExportWindow(self.window(), self.edit_pane)
        # Disable current window
        self.window().setFocusProxy(self.export_window)
        self.export_window.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        self.export_window.show()

    def settings_clicked(self):
        self.settings_window = SettingsWindow(self.window(), self.edit_pane)
        # Disable current window
        self.window().setFocusProxy(self.settings_window)
        self.settings_window.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        self.settings_window.exec()

        # Refresh entry_file as file name might be changed
        self.edit_pane._entry_file.update()
        self.refesh_encryption_switch_button()

    def encryption_switch_clicked(self):
        if self.edit_pane._entry_file.is_encrypted():
            self.edit_pane._entry_file.set_to_unencrypted()
        else:
            self.edit_pane._entry_file.set_to_encrypted()

        self.refesh_encryption_switch_button()

    def refesh_encryption_switch_button(self):
        c = Crypto()
        if not c.is_initialized():
            self.encryption_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["unencrypted"][CONSTANTS.theme])))
            self.encryption_switch_button.setEnabled(False)
            return

        self.encryption_switch_button.setEnabled(True)

        if self.edit_pane._entry_file.is_encrypted():
            self.encryption_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["encrypted"][CONSTANTS.theme])))
        else:
            self.encryption_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["unencrypted"][CONSTANTS.theme])))

    def refresh_stylesheet(self):
        self.setStyleSheet("""
        CustomToolbar{
            background-color: palette(window);
            border: 1px solid palette(dark);
        }
        QPushButton{
            background-color: window;
            border: 0px;
            border-radius: 4px;
        }
        QPushButton:hover{
            background-color: palette(mid);
        }
        QPushButton:pressed{
            background-color: palette(dark);
        }
        QLabel{
            padding-left: 4px;
        }
        QSpinBox{
            background-color: palette(mid);
        }
        
""")