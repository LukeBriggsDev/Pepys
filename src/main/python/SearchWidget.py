from asyncio import TimerHandle
import datetime
from PyQt6 import QtWidgets, QtCore

import re

from EditPane import EditPane
from WebView import WebView
from EntryFile import get_all_entry_files


class SearchWidget(QtWidgets.QWidget):
    def __init__(self, edit_pane: EditPane, web_view: WebView):
        super().__init__()

        self.edit_pane = edit_pane
        self.web_view = web_view

        self.searchText = QtWidgets.QLineEdit(self)
        self.searchText.returnPressed.connect(self.search_clicked)

        searchButton = QtWidgets.QPushButton("Search", self)
        searchButton.clicked.connect(self.search_clicked)

        toolbar = QtWidgets.QToolBar(self)
        toolbar.addWidget(self.searchText)
        toolbar.addWidget(searchButton)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setVisible(False)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Date", "Text"])
        self.table.resizeRowsToContents()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.setSortingEnabled(True)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.table)
        self.setLayout(layout)


    def search_clicked(self):
        self.progress_bar.setVisible(True)

        if self.searchText.text() == "":
            return

        entry_files = get_all_entry_files()
        entry_files.sort(key=lambda x: x.formatted_date)

        results = []
        counter = 0
        for e in entry_files:
            counter = counter + 1
            self.progress_bar.setValue(int(counter *100/ len(entry_files)))
            table_text = self.build_table_text(e.get_content(), self.searchText.text())
            if table_text:
                results.append([e.formatted_date, table_text])

        self.table.clearContents()
        self.table.setRowCount(len(results))
        counter = 0
        for r in results:
            self.table.setItem(counter, 0, QtWidgets.QTableWidgetItem(r[0]),)
            self.table.setItem(counter, 1, QtWidgets.QTableWidgetItem(r[1]))
            counter = counter + 1
        
        self.progress_bar.setVisible(False)
        self.table.resizeColumnsToContents()


    def build_table_text(self, entryText, searchText):
        match_positions = [m.start() for m in re.finditer(searchText, entryText, re.IGNORECASE)]

        if len(match_positions) == 0:
            return ""

        pos = match_positions[0]

        end = pos + 78
        if end >= len(entryText):
            table_text = entryText[pos:]
        else:
            table_text = entryText[pos:end] + "..."

        if len(match_positions) > 1:
            table_text = table_text + "(and " + str(len(match_positions)-1) + " more)"

        return table_text


    def on_row_selected(self):
        if self.table.selectedItems():
            formatted_date = self.table.selectedItems()[0].text()
            date = datetime.datetime.strptime(formatted_date, "%Y-%m-%d")
            self.edit_pane.open_file_from_date(date)
            self.web_view.refresh_page()

    def showEvent(self, e):
        self.searchText.setFocus()