from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from ColorParser import *

if typing.TYPE_CHECKING:
    from main import AppContext


class ExportWindow(QtWidgets.QWidget):
    def __init__(self, main_window, ctx: AppContext):
        super().__init__()
        self.main_window = main_window
        self.setMaximumSize(800, 600)
        self.setMinimumSize(800, 600)

        self.export_options = QtWidgets.QComboBox()
        self.export_options.addItem("HTML")

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.export_options)
        self.setStyleSheet(parse_stylesheet(ctx.get_resource("styles.qss"), ctx.get_resource("colors.json"), ctx.get_resource("config.json")))


    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        self.main_window.setFocusPolicy(QtGui.Qt.StrongFocus)
        self.main_window.setDisabled(False)

