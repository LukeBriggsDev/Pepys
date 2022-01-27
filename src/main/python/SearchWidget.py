from asyncio import TimerHandle
import datetime
from PyQt6 import QtWidgets, QtCore

import re

from EditPane import EditPane
from WebView import WebView
from EntryFile import get_all_entry_files

# Backgournd worker class perfoming search
class SearchWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)
    result_found = QtCore.pyqtSignal(list)

    def __init__(self, searchText):
        super().__init__()
        self._searchText = searchText
        self._break = False

    def interrupt(self):
        self._break = True

    def run(self):
        self._break = False 
        entry_files = get_all_entry_files()
        entry_files.sort(key=lambda x: x.formatted_date)

        counter = 0
        for e in entry_files:
            if self._break:
                break
            counter = counter + 1
            self.progress.emit(int(counter *100/ len(entry_files)))
            table_text = self._build_table_text(e.get_content())
            if table_text:
                self.result_found.emit([e.formatted_date, table_text])

        self.finished.emit()

    def _build_table_text(self, entryText):
        match_positions = [m.start() for m in re.finditer(self._searchText, entryText, re.IGNORECASE)]

        if len(match_positions) == 0:
            return ""

        pos = match_positions[0]

        max_len = 77
        end = pos + max_len
        if end >= len(entryText):
            table_text = entryText[pos:]
        else:
            table_text = entryText[pos:end] + "..."

        if len(match_positions) > 1:
            table_text = table_text + "(and " + str(len(match_positions)-1) + " more)"

        return table_text


class SearchWidget(QtWidgets.QWidget):
    def __init__(self, edit_pane: EditPane, web_view: WebView):
        super().__init__()

        self.edit_pane = edit_pane
        self.web_view = web_view
        self.thread = QtCore.QThread(parent= self)
        self.thread.finished.connect(self.search_finished)

        self.searchText = QtWidgets.QLineEdit(self)
        self.searchText.returnPressed.connect(self.search_clicked)

        self.searchButton = QtWidgets.QPushButton("Search", self)
        self.searchButton.clicked.connect(self.search_clicked)

        toolbar = QtWidgets.QToolBar(self)
        toolbar.addWidget(self.searchText)
        toolbar.addWidget(self.searchButton)

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
        if self.thread.isRunning():
            self.worker.interrupt()
            return

        if self.searchText.text() == "":
            return

        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        self.table.clearContents()
        self.table.setRowCount(0)

        # Run search in a background thread
        self.worker = SearchWorker(self.searchText.text())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.result_found.connect(self.result_found)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.start()

        self.searchButton.setText("Stop")
        self.searchText.setEnabled(False)


    def on_row_selected(self):
        if self.table.selectedItems():
            formatted_date = self.table.selectedItems()[0].text()
            date = datetime.datetime.strptime(formatted_date, "%Y-%m-%d")
            self.edit_pane.open_file_from_date(date)
            self.web_view.refresh_page()


    def update_progress(self, progress):
        self.progress_bar.setValue(progress)


    def result_found(self, result):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        self.table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(result[0]),)
        self.table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(result[1]))
        self.table.resizeColumnsToContents()


    def search_finished(self):
        self.progress_bar.setVisible(False)
        self.searchButton.setText("Search")
        self.searchText.setEnabled(True)


    def showEvent(self, e):
        self.searchText.setFocus()

    def closeEvent(self, event) -> None:
        if self.thread.isRunning():
            self.worker.interrupt()
