import datetime
from PyQt6 import QtWidgets, QtCore

import re

from EditPane import EditPane
from WebView import WebView
from EntryFile import EntryFile, get_all_entry_files

# Background worker class collecting data
class TagAnalysisWorker(QtCore.QObject):
    
    progress = QtCore.pyqtSignal(int)
    result_collected = QtCore.pyqtSignal(list, list)
    finished = QtCore.pyqtSignal()

    def __init__(self, tag_name, key_value_selection, interval_selection):
        super().__init__()
        self._tag_name = tag_name
        self._key_value_selection = key_value_selection
        self._interval_selection = interval_selection
        self._break = False


    def interrupt(self):
        self._break = True


    def run(self):
        self._break = False
        if not self._tag_name:
            self.finished.emit()
            return

        entry_files = get_all_entry_files()
        entry_files = list(self.filter_by_tag(entry_files, self._tag_name))
        
        if self._break:
            self.finished.emit()
            return

        entry_files.sort(key=lambda x: x.formatted_date)
        
        if self._break:
            self.finished.emit()
            return

        if self._key_value_selection == 0:
            histo = self.create_histogram_data(self._interval_selection, entry_files)
            self.result_collected.emit([self._interval_selection, "count"], histo)
        elif self._key_value_selection == 1:
            data = self.create_values_data(self._interval_selection, self._tag_name, entry_files)
            self.result_collected.emit([self._interval_selection, self._tag_name], data)
        else: 
            data = self.create_value_sum_data(self._interval_selection, self._tag_name, entry_files)
            self.result_collected.emit([self._interval_selection, self._tag_name], data)

        self.finished.emit()


    def filter_by_tag(self,entry_files, tag_name):
        for i,entry_file in enumerate(entry_files):
            if entry_file.has_tag(tag_name): 
                yield entry_file
                self.progress.emit(i*100/len(entry_files))
                if (self._break):
                    return

    # Create a histogram of the entry file tag with the given time interval
    def create_histogram_data(self, interval_name, entry_files):
        d = {}
        for e in entry_files:
            k = self.get_histogram_key_name(interval_name, e)
            if k in d:
                d[k] = d[k] + 1
            else:
                d[k] = 1
        return d.items()

    def get_histogram_key_name(self, interval_name, entry_file):
        if interval_name == "week":
            return entry_file.get_year_with_week()
        if interval_name == "month":
            return entry_file.get_year_with_month()
        if interval_name == "year":
            return entry_file.get_year()
        return entry_file.formatted_date

    # Get a list of the values of the entry file tag within the given time intervals
    def create_values_data(self, key_name, tag_name, entry_files):
        d = {}
        for e in entry_files:
            k = self.get_histogram_key_name(key_name, e)
            if k in d:
                d[k] = d[k] + ", " + str(e.get_tag_value(tag_name))
            else:
                d[k] = str(e.get_tag_value(tag_name))
        return d.items()

    # Get the value sum of the entry file tags within the given time intervals
    def create_value_sum_data(self, key_name, tag_name, entry_files):
        d = {}
        for e in entry_files:
            k = self.get_histogram_key_name(key_name, e)
            if k in d:
                v = e.get_tag_value(tag_name)
                if isinstance(v, (int, float)) and isinstance(d[k], (int, float)):
                    d[k] = d[k] + v
                else:
                    # If value is not numeric just create comma separated list
                    d[k] = d[k] + ", " + str(v)
            else:
                d[k] = e.get_tag_value(tag_name)
        return d.items()


class TagAnalysisWidget(QtWidgets.QWidget):
    def __init__(self, edit_pane: EditPane, web_view: WebView):
        super().__init__()

        self.edit_pane = edit_pane
        self.web_view = web_view
        self.thread = QtCore.QThread(parent= self)
        self.thread.finished.connect(self.collection_finished)

        self.tag_name = QtWidgets.QLineEdit(self)

        self.key_value_selection = QtWidgets.QComboBox(self)
        self.key_value_selection.setMinimumWidth(90)
        self.key_value_selection.addItem("count")
        self.key_value_selection.addItem("values")
        self.key_value_selection.addItem("value sum")

        self.interval_selection = QtWidgets.QComboBox(self)
        self.interval_selection.setMinimumWidth(90)
        self.interval_selection.addItem("day")
        self.interval_selection.addItem("week")
        self.interval_selection.addItem("month")
        self.interval_selection.addItem("year")

        self.search_button = QtWidgets.QPushButton("Show", self)
        self.search_button.setMinimumWidth(60)
        self.search_button.clicked.connect(self.search_clicked)

        toolbar = QtWidgets.QToolBar(self)
        toolbar.addWidget(QtWidgets.QLabel("For tag ", self))
        toolbar.addWidget(self.tag_name)
        toolbar.addWidget(QtWidgets.QLabel(" show ", self))
        toolbar.addWidget(self.key_value_selection)
        toolbar.addWidget(QtWidgets.QLabel(" by ",self))
        toolbar.addWidget(self.interval_selection)
        toolbar.addWidget(self.search_button)

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
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.setSortingEnabled(True)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setStyleSheet(
            """
            QToolBar {
                background-color: palette(base);
                border: palette(window);
            }
            QLineEdit {
                background-color: palette(base);
                border: 2px solid palette(dark);
                height: 24px;
            } 
            QPushButton {
                background-color: palette(button);
                border: 2px solid palette(dark);
                height: 24px;
                padding-left: 4px;
                padding-right: 4px;
            }
            QPushButton:pressed {
                background-color: palette(dark);     
            }

            QHeaderView::section {
                background-color: palette(button);
            }
            """
        )


    def search_clicked(self):
        if self.thread.isRunning():
            self.worker.interrupt()
            return

        if self.tag_name.text() == "":
            return

        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        self.table.clearContents()
        self.table.setRowCount(0)

        # Run search in a background thread
        self.worker = TagAnalysisWorker(self.tag_name.text(), 
            self.key_value_selection.currentIndex(),
            self.interval_selection.currentText())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.result_collected.connect(self.result_collected)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.start()

        self.search_button.setText("Stop")
        self.tag_name.setEnabled(False)
        self.key_value_selection.setEnabled(False)
        self.interval_selection.setEnabled(False)
       

    def result_collected(self, header_lables, data):
        self.table.setHorizontalHeaderLabels(header_lables)
        self.table.clearContents()
        self.table.setRowCount(len(data))
        counter = 0
        for d in data:
            self.table.setItem(counter, 0, QtWidgets.QTableWidgetItem(d[0]))
            self.table.setItem(counter, 1, QtWidgets.QTableWidgetItem(str(d[1])))
            counter = counter + 1

    
    def update_progress(self, progress):
        self.progress_bar.setValue(progress)


    def collection_finished(self):
        self.progress_bar.setVisible(False)
        self.search_button.setText("Show")
        #Todo: Enable GUI elements
        self.tag_name.setEnabled(True)
        self.key_value_selection.setEnabled(True)
        self.interval_selection.setEnabled(True)


    def showEvent(self, e):
        self.tag_name.setFocus()
        
