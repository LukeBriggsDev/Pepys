from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui, QtCore

import CONSTANTS
from CONSTANTS import get_resource
from ColorParser import *

if typing.TYPE_CHECKING:
    pass


class ThemeSwitchButton(QtWidgets.QPushButton):
    """Button for toggling the current application theme"""
    def __init__(self):
        """Constructor
        :param ctx: AppContext containing global functions and variables
        """
        super().__init__()
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)

        # Read current theme
        with open(get_resource("config.json"), "r") as config:
            theme = json.loads(config.read())["theme"]

        # Set corresponding icon
        if theme == "light":
            self.setIcon(QtGui.QIcon(get_resource("icons/brightness-high.svg")))
        else:
            self.setIcon(QtGui.QIcon(get_resource("icons/brightness-low-fill.svg")))
        self.setToolTip("Change Theme")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)

        # Read current icoon
        with open(get_resource("config.json"), "r") as config:
            current_config = json.loads(config.read())

        current_theme = current_config["theme"]

        # Toggle theme
        if current_theme == "light":
            CONSTANTS.theme = "dark"
        else:
            CONSTANTS.theme = "light"

        self.setIcon(QtGui.QIcon(get_resource(CONSTANTS.icons["theme_switch"][CONSTANTS.theme])))

        # Save change
        with open(get_resource("config.json"), "w") as config:
            current_config["theme"] = CONSTANTS.theme
            config.write(json.dumps(current_config, sort_keys=True, indent=4))

        main_window = self.parentWidget().parentWidget()
        # Set main window stylesheet
        main_window.setStyleSheet(parse_stylesheet(get_resource("styles.qss"), get_resource("colors.json"), get_resource("config.json")))

        # Refresh web_view
        self.parentWidget().preview_button.refresh_page()
        # Call resize event to cause update
        QtCore.QCoreApplication.postEvent(main_window, QtGui.QResizeEvent(main_window.size(), main_window.size()))