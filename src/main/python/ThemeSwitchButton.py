from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui, QtCore

from ColorParser import *

if typing.TYPE_CHECKING:
    from main import AppContext


class ThemeSwitchButton(QtWidgets.QPushButton):
    """Button for toggling the current application theme"""
    def __init__(self, ctx: AppContext):
        """Constructor
        :param ctx: AppContext containing global functions and variables
        """
        super().__init__()
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.ctx = ctx

        # Read current theme
        with open(ctx.get_resource("config.json"), "r") as config:
            theme = json.loads(config.read())["theme"]

        # Set corresponding icon
        if theme == "light":
            self.setIcon(QtGui.QIcon(ctx.get_resource("icons/brightness-high.svg")))
        else:
            self.setIcon(QtGui.QIcon(ctx.get_resource("icons/brightness-low-fill.svg")))
        self.setToolTip("Change Theme")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)

        # Read current icoon
        with open(self.ctx.get_resource("config.json"), "r") as config:
            current_config = json.loads(config.read())

        current_theme = current_config["theme"]

        # Toggle theme
        if current_theme == "light":
            self.ctx.theme = "dark"
        else:
            self.ctx.theme = "light"

        self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["theme_switch"][self.ctx.theme])))

        # Save change
        with open(self.ctx.get_resource("config.json"), "w") as config:
            current_config["theme"] = self.ctx.theme
            config.write(json.dumps(current_config))

        main_window = self.parentWidget().parentWidget()
        # Set main window stylesheet
        main_window.setStyleSheet(parse_stylesheet(self.ctx.get_resource("styles.qss"), self.ctx.get_resource("colors.json"), self.ctx.get_resource("config.json")))

        # Refresh web_view
        self.parentWidget().preview_button.refresh_page()
        # Call resize event to cause update
        QtCore.QCoreApplication.postEvent(main_window, QtGui.QResizeEvent(main_window.size(), main_window.size()))