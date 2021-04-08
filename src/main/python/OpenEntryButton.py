from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext
    from EditPane import EditPane

class OpenEntryButton(QtWidgets.QPushButton):
    def __init__(self, edit_pane: EditPane, ctx: AppContext):
        super().__init__()
        self.edit_pane = edit_pane
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMaximumSize(32, 32)
        self.setToolTip("Open Entry")
        self.setWhatsThis("Click this to select an entry via a calendar")
        self.setIcon(QtGui.QIcon(ctx.get_resource("icons/calendar.svg")))

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        self.open_date_picker()



    def open_date_picker(self) -> None:
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

# self.date_dialog = CalendarFileSelector(self.edit_pane, self.ctx)
#
# self.date_dialog.show()