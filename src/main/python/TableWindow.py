from PySide2 import QtWidgets, QtGui
import CONSTANTS
from CONSTANTS import get_resource
from ColorParser import parse_stylesheet

class TableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.table_cells = []
        self.setStyleSheet(parse_stylesheet(get_resource("styles.qss"), CONSTANTS.theme))
        self.table_option_layout = QtWidgets.QFormLayout()
        self.row_spinbox = QtWidgets.QSpinBox()
        self.row_spinbox.setMinimum(1)
        self.row_spinbox.valueChanged.connect(self.update_table)
        self.column_spinbox = QtWidgets.QSpinBox()
        self.column_spinbox.setMinimum(1)
        self.table_type = QtWidgets.QComboBox()
        self.table_type.addItem("Booktabs")
        self.table_type.addItem("Grid")
        self.table_option_layout.addRow("Table Style:", self.table_type)
        self.include_headers = QtWidgets.QCheckBox()
        self.include_headers.setFixedSize(24, 24)
        self.table_option_layout.addRow("Use first row as header: ", self.include_headers)
        self.column_spinbox.valueChanged.connect(self.update_table)
        self.table_option_layout.addRow("Rows:", self.row_spinbox)
        self.table_option_layout.addRow("Columns: ", self.column_spinbox)
        self.table_grid = QtWidgets.QGridLayout()
        self.table_option_layout.addRow("Table: ", self.table_grid)
        self.setLayout(self.table_option_layout)
        self.update_table()

    def update_table(self, *kwargs):
        # FIXME: All data in table is cleared on update
        self.table_cells = []
        self.table_option_layout.removeRow(self.table_grid)
        self.table_grid = QtWidgets.QGridLayout()
        self.table_option_layout.insertRow(4, "Table: ", self.table_grid)
        for row in range(self.row_spinbox.value()):
            new_row = []
            for col in range(self.column_spinbox.value()):
                new_cell = QtWidgets.QTextEdit()
                new_cell.setStyleSheet("border: 1px solid black")
                new_cell.setMinimumSize(100, 80)
                self.table_grid.addWidget(new_cell, row, col)
                new_row.append(new_cell)
            self.table_cells.append(new_row)