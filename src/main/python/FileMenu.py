from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from CalendarFileSelector import CalendarFileSelector


class FileMenu(QtWidgets.QMenu):
    """Setup menu for file options to be added to a menu bar."""

    def __init__(self, edit_pane: EditPane) -> None:
        super().__init__("File")
        self.edit_pane = edit_pane

        # Add new file action
        new_file_action = self.addAction("New")
        new_file_action.triggered.connect(self.new_file)

        # Add open file action
        open_file_action = self.addAction("Open")
        open_file_action.triggered.connect(self.open_file)

        open_file_action = self.addAction("Open Entry")
        open_file_action.triggered.connect(self.open_file_date)

        # Add save file action
        save_file_action = self.addAction("Save")
        save_file_action.triggered.connect(self.save_file)

    def new_file(self) -> None:
        print("NewFile")

    def open_file_date(self) -> None:
        self.date_dialog = CalendarFileSelector(self.edit_pane)
        self.date_dialog.layout = QtWidgets.QVBoxLayout()
        calendar = QtWidgets.QCalendarWidget()
        self.date_dialog.layout.addWidget(calendar)
        self.date_dialog.setMinimumSize(480, 480)
        self.date_dialog.setMaximumSize(480, 480)
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
