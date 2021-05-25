from __future__ import annotations

import typing

from PyQt5 import QtWidgets, QtGui, QtCore

from WebView import WebView
from EntryExplorer import EntryExplorer
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
        self.favorite_button.setMaximumSize(32, 32)
        self.refresh_favorite()
        self.setToolTip("Favourite")
        self.favorite_button.clicked.connect(self.favorite_clicked)

        # Preview button
        self.preview_button = QtWidgets.QPushButton()
        self.preview_button.setMinimumSize(32, 32)
        self.preview_button.setMaximumSize(32, 32)
        self.preview_button.setIcon(QtGui.QIcon(get_resource("icons/book.svg")))
        self.preview_button.setToolTip("Preview")
        self.preview_button.clicked.connect(self.preview_clicked)

        # About button
        self.about_button = QtWidgets.QPushButton()
        self.about_button.setMinimumSize(32, 32)
        self.about_button.setMaximumSize(32, 32)
        self.about_button.setIcon(QtGui.QIcon(get_resource("icons/question.svg")))
        self.about_button.setToolTip("About")
        self.about_button.clicked.connect(self.about_clicked)

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

        # Theme switch button
        self.theme_switch_button = QtWidgets.QPushButton()
        self.theme_switch_button.setMinimumSize(32, 32)
        self.theme_switch_button.setMaximumSize(32, 32)
        self.theme_switch_button.setToolTip("Change theme")
        self.theme_switch_button.clicked.connect(self.theme_switch)
        #Read current theme

        # Add buttons to layout
        self.addWidget(self.open_entry_button)
        self.addWidget(self.favorite_button)
        self.addWidget(self.export_button)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.addWidget(spacer)
        self.addWidget(self.theme_switch_button)
        self.addWidget(self.insert_button)
        self.addWidget(self.preview_button)
        self.addWidget(self.about_button)
        self.refresh_stylesheet()

    def changeEvent(self, event:QtCore.QEvent) -> None:
        # Change button icons to match theme
        if event.type() == QtCore.QEvent.PaletteChange:
            self.open_entry_button.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["open_entry"][CONSTANTS.theme])))
            self.refresh_favorite()

            # Refresh preview icon
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
        self.about_window.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.about_window.show()

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


        current_theme = CONSTANTS.theme

        if current_theme == "light":
            QtWidgets.QApplication.setPalette(CONSTANTS.Colors.getDarkpalette())
            CONSTANTS.theme = "dark"
        elif CONSTANTS.light_palette.color(QtGui.QPalette.Active, QtGui.QPalette.Base).lightness() > 122:
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
        self.export_window.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.export_window.show()

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
        
""")