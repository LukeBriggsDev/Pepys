from PySide2 import QtWidgets, QtGui, QtCore
import CONSTANTS
from CONSTANTS import get_resource
from ColorParser import parse_stylesheet
from ColorParser import text_to_rgb
import sys

class TableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.table_cells = []
        self.setMinimumSize(800, 600)

        # Workaround for button elements not changing BG on MacOS
        if QtWidgets.QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base).lightness() < 122 and sys.platform == "darwin":
            self.setStyleSheet(
                """
                QPushButton{
                    color: palette(base);
                }
                QComboBox{
                    color: palette(base);
                }
                QComboBox QAbstractItemView{
                    background-color: palette(text);
                }
                """
            )


        self.table_option_layout = QtWidgets.QFormLayout()
        self.row_spinbox = QtWidgets.QSpinBox()
        self.row_spinbox.setMinimum(1)
        self.row_spinbox.setMinimumWidth(100)
        self.row_spinbox.valueChanged.connect(self.update_table)
        self.column_spinbox = QtWidgets.QSpinBox()
        self.column_spinbox.setMinimum(1)
        self.column_spinbox.setMinimumWidth(100)
        self.table_type = QtWidgets.QComboBox()
        self.table_type.addItem("Booktabs")
        self.table_type.addItem("Grid")
        self.table_option_layout.addRow("Table Style:", self.table_type)
        self.include_headers = QtWidgets.QCheckBox()
        self.include_headers.stateChanged.connect(self.set_headers)
        self.include_headers.setFixedSize(24, 24)
        self.table_option_layout.addRow("Use first row as header: ", self.include_headers)
        self.column_spinbox.valueChanged.connect(self.update_table)
        self.table_option_layout.addRow("Rows:", self.row_spinbox)
        self.table_option_layout.addRow("Columns: ", self.column_spinbox)
        self.table_widget = QtWidgets.QTableWidget()
        self.table_option_layout.addRow("Table: ", self.table_widget)
        self.table_widget.cellChanged.connect(self.cell_changed)
        self.setLayout(self.table_option_layout)
        self.update_table()

    def update_table(self, *kwargs):
        # FIXME: All data in table is cleared on update
        self.table_widget.setRowCount(self.row_spinbox.value())
        self.table_widget.setColumnCount(self.column_spinbox.value())

    def cell_changed(self, row, col):
        if row == 0:
            self.set_headers(self.include_headers.checkState())
        max_size = ""
        for i in range(self.table_widget.rowCount()):
            if self.table_widget.item(i, col) is not None and \
                    self.table_widget.fontMetrics().horizontalAdvance(self.table_widget.item(i, col).text()) > self.table_widget.fontMetrics().horizontalAdvance(max_size):
                max_size = self.table_widget.item(i, col).text()
        self.table_widget.setColumnWidth(col, self.table_widget.fontMetrics().horizontalAdvance(max_size) + 32)

    def set_headers(self, state: QtCore.Qt.CheckState):

            for col in range(self.table_widget.columnCount()):
                cell = self.table_widget.item(0, col)
                if cell is not None:
                    if state == QtCore.Qt.CheckState.Checked:
                        font = cell.font()
                        font.setBold(True)
                        cell.setBackground(QtWidgets.QApplication.palette().color(QtGui.QPalette.Window))
                        cell.setFont(font)
                    else:
                        self.table_widget.item(0, col)
                        font = cell.font()
                        font.setBold(False)
                        cell.setBackground(QtWidgets.QApplication.palette().color(QtGui.QPalette.Base))
                        cell.setFont(font)