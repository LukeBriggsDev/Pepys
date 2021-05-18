from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui, QtCore

from WebView import WebView
import json
import pathlib
import shutil

from ColorParser import parse_stylesheet

if typing.TYPE_CHECKING:
    pass

from EditPane import EditPane
from AboutWindow import AboutWindow
from ExportWindow import ExportWindow
from TableWindow import TableWindow
from CONSTANTS import get_resource
from CalendarFileSelector import CalendarFileSelector
import CONSTANTS

class CustomToolbar(QtWidgets.QToolBar):
    """Menu bar to appear with MainWindow"""
    def __init__(self, edit_pane: EditPane, web_view: WebView) -> None:
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
        self.favorite_button.setMinimumSize(32, 32)
        self.refresh_favorite()
        self.setToolTip("Favourite")
        self.favorite_button.clicked.connect(self.favorite_clicked)

        # Preview button
        self.preview_button = QtWidgets.QPushButton()
        self.preview_button.setMinimumSize(32, 32)
        self.preview_button.setMinimumSize(32, 32)
        self.preview_button.setIcon(QtGui.QIcon(get_resource("icons/book.svg")))
        self.preview_button.setToolTip("Preview")
        self.preview_button.clicked.connect(self.preview_clicked)

        # About button
        self.about_button = QtWidgets.QPushButton()
        self.about_button.setMinimumSize(32, 32)
        self.about_button.setMinimumSize(32, 32)
        self.about_button.setIcon(QtGui.QIcon(get_resource("icons/question.svg")))
        self.about_button.setToolTip("About")
        self.about_button.clicked.connect(self.about_clicked)

        # Export Button
        self.export_button = QtWidgets.QPushButton()
        self.export_button.setMinimumSize(32, 32)
        self.export_button.setMinimumSize(32, 32)
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

        # Theme switch button
        self.theme_switch_button = QtWidgets.QPushButton()
        self.theme_switch_button.setMinimumSize(32, 32)
        self.theme_switch_button.setMinimumSize(32, 32)
        self.theme_switch_button.setToolTip("Change theme")
        self.theme_switch_button.clicked.connect(self.theme_switch)
        # Read current theme
        with open(get_resource("config.json"), "r") as config:
            theme = json.loads(config.read())["theme"]
        # Set corresponding icon
        if theme == "light":
            self.theme_switch_button.setIcon(QtGui.QIcon(get_resource("icons/brightness-high.svg")))
        else:
            self.theme_switch_button.setIcon(QtGui.QIcon(get_resource("icons/brightness-low-fill.svg")))
        self.theme_switch_button.setToolTip("Change Theme")

        # Add buttons to layout
        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        self.addWidget(self.export_button)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.insert_button)
        self.addWidget(self.preview_button)
        self.addWidget(self.theme_switch_button)
        self.addWidget(self.about_button)


    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change button icons to match theme
        if event.type() is QtCore.QEvent.Type.StyleChange:
            self.open_entry_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["open_entry"][CONSTANTS.theme])))
            self.refresh_favorite()

            # Refresh previw icon
            if not self.web_view.isVisible():
                self.preview_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview"][CONSTANTS.theme])))
            else:
                self.preview_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["preview_stop"][CONSTANTS.theme])))

            self.about_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["about"][CONSTANTS.theme])))
            self.insert_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["plus"][CONSTANTS.theme])))
            self.theme_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["theme_switch"][CONSTANTS.theme])))
            self.export_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["export"][CONSTANTS.theme])))

    def about_clicked(self):
        # Create about dialog
        self.about_window = AboutWindow(self.window())

        # Disable main window
        self.window().setFocusProxy(self.about_window)
        self.window().setDisabled(True)
        self.about_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.about_window.show()

    def open_entry_clicked(self):
        """Open calendar dialog and disable main window"""
        self.date_dialog = CalendarFileSelector(self.edit_pane, self.web_view)
        self.window().setFocusProxy(self.date_dialog)
        self.window().setDisabled(True)
        self.date_dialog.setFocusPolicy(QtGui.Qt.StrongFocus)

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
        self.insert_menu.setStyleSheet(parse_stylesheet(get_resource("styles.qss"),CONSTANTS.theme))
        self.insert_menu.addAction("Insert image", self.edit_pane.insert_image)
        self.insert_menu.addAction("Insert table", self.open_table_options)
        self.insert_menu.popup(self.mapToGlobal(self.insert_button.pos() + QtCore.QPoint(- self.insert_button.width(), self.insert_button.height())))
        pass

    def open_table_options(self):
        self.table_option_dialog = TableWindow()
        insert_button = QtWidgets.QPushButton("Create Table")
        insert_button.clicked.connect(self.table_handler)
        self.table_option_dialog.layout().addWidget(insert_button)
        self.table_option_dialog.exec_()

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

    def theme_switch(self):

        # Read current icon
        with open(get_resource("config.json"), "r") as config:
            current_config = json.loads(config.read())

        current_theme = current_config["theme"]

        # Toggle theme
        if current_theme == "light":
            CONSTANTS.theme = "dark"
        else:
            CONSTANTS.theme = "light"

        self.theme_switch_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["theme_switch"][CONSTANTS.theme])))

        # Save change
        with open(get_resource("config.json"), "w") as config:
            current_config["theme"] = CONSTANTS.theme
            config.write(json.dumps(current_config, sort_keys=True, indent=4))

        main_window = self.parentWidget()
        # Set main window stylesheet
        main_window.setStyleSheet(parse_stylesheet(get_resource("styles.qss"), CONSTANTS.theme))

        # Refresh web_view
        self.web_view.refresh_page()
        # Refresh edit pane
        self.edit_pane.markdownHighlighter.rehighlight()
        # Call resize event to cause update
        QtCore.QCoreApplication.postEvent(main_window, QtGui.QResizeEvent(main_window.size(), main_window.size()))

    def export_clicked(self):
        self.export_window = ExportWindow(self.window())
        # Disable current window
        self.window().setFocusProxy(self.export_window)
        self.window().setDisabled(True)
        self.export_window.setFocusPolicy(QtGui.Qt.StrongFocus)

        self.export_window.show()
