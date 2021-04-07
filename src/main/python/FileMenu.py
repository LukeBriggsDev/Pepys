from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from CalendarFileSelector import CalendarFileSelector
import typing
if typing.TYPE_CHECKING:
    from AppContext import AppContext


class FileMenu(QtWidgets.QMenu):
    """Setup menu for file options to be added to a menu bar."""

    def __init__(self, edit_pane: EditPane, ctx: AppContext) -> None:
        super().__init__("File")
        self.edit_pane = edit_pane
        self.ctx = ctx

        with open(ctx.get_resource("MenuBarStyle.qss")) as file:
            stylesheet = file.read()


        open_file_action = self.addAction("Open Entry")
        open_file_action.triggered.connect(self.open_file_date)


        self.setStyleSheet(stylesheet)

    def new_file(self) -> None:
        print("NewFile")

    def open_file_date(self) -> None:
        self.date_dialog = CalendarFileSelector(self.edit_pane, self.ctx)

        self.date_dialog.show()


    def open_file(self) -> None:
        """Open file in text edit, called when open_file_action clicked"""

        # Get file from file dialog
        filename = QtWidgets.QFileDialog.getOpenFileName(self)

        with open(filename[0], 'r') as file:
            self.edit_pane.set_current_file(filename[0])

        print("OpenFile")

    def save_file(self) -> None:
        self.edit_pane.save_current_file()
