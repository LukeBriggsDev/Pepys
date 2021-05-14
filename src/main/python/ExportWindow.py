from __future__ import annotations

import typing
from threading import Thread

from PySide2 import QtWidgets, QtGui, QtCore

from CONSTANTS import get_resource
from ColorParser import *
import pypandoc
from pathlib import Path
import PyPDF4
import os
import CONSTANTS
import shutil

if typing.TYPE_CHECKING:
    pass

class ExportWindow(QtWidgets.QWidget):
    """Window for selecting export options"""

    output_formats = {
        "Word Document": {"type": "docx", "ext": "docx"},
        "EBook": {"type": "epub", "ext": "epub"},
        "HTML": {"type": "html", "ext": "html"},
        "PDF": {"type": "pdf", "ext": "pdf"},
        "Latex": {"type": "latex", "ext": "tex"},
        "OpenOffice Text Document": {"type": "odt", "ext": "odt"},
        "Plain Text": {"type": "plain", "ext": "txt"},
        "PowerPoint Slide Show": {"type": "pptx", "ext": "pptx"},
        "Rich Text Format": {"type": "rtf", "ext": "rtf"},
        "reStructuredText": {"type": "rst", "ext": "rst"},
    }

    def __init__(self, main_window):
        super().__init__()
        # Window options
        self.main_window = main_window
        self.setMaximumSize(640, 240)
        self.setMinimumSize(640, 240)
        self.setWindowFlag(QtGui.Qt.Dialog)
        formLayout = QtWidgets.QFormLayout()

        self.export_options = QtWidgets.QComboBox()


        for output_format in sorted(self.output_formats.keys(), key=str.lower):
            self.export_options.addItem(output_format)
        formLayout.addRow("Export Format: ", self.export_options)

        # Selecting export date
        self.date_select_layout = QtWidgets.QGridLayout()

        self.date_options = QtWidgets.QComboBox()
        self.date_options.addItems(["Current Entry", "Custom Range", "All Entries"])
        self.date_select_layout.addWidget(self.date_options, 0, 0, 2, 1)
        self.date_options.currentTextChanged.connect(self.disable_custom_date)

        self.custom_date_layout = QtWidgets.QFormLayout()
        self.start_date_widget = QtWidgets.QDateEdit()
        self.start_date_widget.setDisplayFormat("yyyy-MM-dd")
        self.start_date_widget.setDate(QtCore.QDate.currentDate())
        self.end_date_widget = QtWidgets.QDateEdit()
        self.end_date_widget.setDisplayFormat("yyyy-MM-dd")
        self.end_date_widget.setDate(QtCore.QDate.currentDate())
        self.custom_date_layout.addRow("Start Date:", self.start_date_widget)
        self.start_date_widget.dateChanged.connect(self.end_date_widget.setMinimumDate)
        self.custom_date_layout.addRow("End Date:", self.end_date_widget)
        self.end_date_widget.dateChanged.connect(self.start_date_widget.setMaximumDate)
        self.date_select_layout.addLayout(self.custom_date_layout, 2, 0, 1, self.custom_date_layout.rowCount())


        formLayout.addRow("Select Date: ", self.date_select_layout)

        self.will_collate = QtWidgets.QCheckBox()
        self.will_collate.setFixedSize(38, 38)
        formLayout.addRow("Collate together:", self.will_collate)

        self.setLayout(formLayout)

        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.clicked.connect(self.export_clicked)
        self.layout().addWidget(self.export_button)

        self.setStyleSheet(parse_stylesheet(get_resource("styles.qss"),CONSTANTS.theme))

        self.setWindowTitle("Export")

        self.disable_custom_date()
        self.export_options.currentTextChanged.connect(self.format_option_change)
        self.format_option_change(None)

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        # Re-enable main window
        self.main_window.setFocusPolicy(QtGui.Qt.StrongFocus)
        self.main_window.setDisabled(False)

    def format_option_change(self, new_text: str):
        if new_text == "HTML" or new_text == "PDF":
            self.will_collate.setEnabled(True)
        else:
            self.will_collate.setEnabled(False)
            self.will_collate.setChecked(False)

    def disable_custom_date(self, *kwargs):
        if len(kwargs) == 0 or kwargs[0] != "Custom Range":
            self.start_date_widget.setEnabled(False)
            self.end_date_widget.setEnabled(False)
        else:
            self.start_date_widget.setEnabled(True)
            self.end_date_widget.setEnabled(True)

    def export_clicked(self):
        self.export_diary()
        self.setEnabled(True)


    def export_diary(self):

        # Load dialog
        self.load_dialog = QtWidgets.QDialog(self)
        self.load_dialog.setWindowModality(QtGui.Qt.WindowModal)
        self.load_dialog.setMinimumSize(400, 100)
        self.load_dialog.setWindowTitle("Exporting...")
        progress_label = QtWidgets.QLabel()
        progress_label.setAlignment(QtGui.Qt.AlignCenter)
        progress_bar = QtWidgets.QProgressBar()
        self.load_dialog.setLayout(QtWidgets.QVBoxLayout())
        self.load_dialog.layout().setAlignment(QtGui.Qt.AlignTop)
        self.load_dialog.layout().addWidget(progress_label)
        self.load_dialog.layout().addWidget(progress_bar)
        self.load_dialog.show()
        self.setDisabled(True)
        self.load_dialog.setEnabled(True)

        with open(get_resource("config.json"), "r") as file:
            directory = json.loads(file.read())["diary_directory"]

        diary_entries = list(Path(directory).rglob("*-*-*.[mM][dD]"))

        # Custom Range
        if self.date_options.currentText() == "Custom Range":
            diary_entries = [entry for entry in diary_entries
                             if self.start_date_widget.date().toString("yyyy-MM-dd") <= entry.name[:-3] <= self.end_date_widget.date().toString("yyyy-MM-dd")]

        # Current Date
        if self.date_options.currentText() == "Current Entry":
            diary_entries = list(Path(directory).rglob(f"{QtCore.QDate.currentDate().toString('yyyy-MM-dd')}.[mM][dD]"))

        format = self.output_formats[self.export_options.currentText()]


        pdoc_args = ["--standalone",
                     f"--katex={get_resource('katex/')}"]

        if format["type"] == "pdf":
            # Convert to html before pdf to apply css
            pdoc_args.append("-thtml")
            pass

        if format["type"] == "html" or format["type"]=="pdf":
            with open(get_resource("parsed_stylesheet.css"), "w+") as f:
                f.write(parse_stylesheet(get_resource("ViewPaneStyle.css"), "light"))
            pdoc_args.append("--css="+get_resource("parsed_stylesheet.css"))
            pdoc_args.append("--self-contained")


        progress_label.setText("Converting to " + str(format["type"]))
        progress_bar.setMaximum(len(diary_entries))
        QtWidgets.QApplication.processEvents()
        finished = 0
        # Conversion
        for entry in diary_entries:
            if self.load_dialog.isVisible():
                os.chdir(entry.parent.as_posix())
                try:
                    pypandoc.convert_file(entry.as_posix(), format["type"],
                                          outputfile=(entry.parent.as_posix() + "/" + entry.name[:-3] + "." + format["ext"]),
                                          extra_args=pdoc_args)
                except RuntimeError as err:
                    progress_label.setText("ERROR IN FILE " + entry.name)
                    QtWidgets.QApplication.processEvents()
                    print(err)
                finished += 1
                progress_label.setText(str(finished) + "/" + str(len(diary_entries)))
                progress_bar.setValue(finished)
                QtWidgets.QApplication.processEvents()
            else:
                return 1
        progress_label.setText("Conversion finished")
        QtWidgets.QApplication.processEvents()

        if self.will_collate.isChecked():
            # Collate pdfs together into one pdf
            if format["type"] == "pdf":
                progress_label.setText("Starting pdf collation")
                QtWidgets.QApplication.processEvents()
                file_merger = PyPDF4.PdfFileMerger(strict=False)
                pdf_list = sorted([Path(entry.as_posix()[:-3] + ".pdf") for entry in diary_entries], key=lambda x: x.name)
                for pdf in pdf_list:
                    progress_label.setText(pdf.name)
                    QtWidgets.QApplication.processEvents()
                    file_merger.append(pdf.as_posix(), pdf.name[:-4], import_bookmarks=False)
                file_merger.write(directory + "/diary.pdf")
                progress_label.setText("pdf collation finished")
                QtWidgets.QApplication.processEvents()

            if format["type"] == "html":
                progress_label.setText("Starting html collation")
                QtWidgets.QApplication.processEvents()
                html_list = sorted([Path(entry.as_posix()[:-3] + ".html") for entry in diary_entries], key=lambda x: x.name)
                html = ""
                try:
                    os.mkdir(os.path.join(Path(directory), "html_export"))
                except FileExistsError:
                    shutil.rmtree(os.path.join(Path(directory), "html_export"), ignore_errors=True)
                    os.mkdir(os.path.join(Path(directory), "html_export"))

                for document in html_list:
                    shutil.move(document, os.path.join(Path(directory), "html_export", document.name))

                with open(os.path.join(Path(directory), "html_export", "_index.html"), "w") as f:
                    shutil.copyfile(get_resource("parsed_stylesheet.css"), os.path.join(Path(directory), "html_export", "styles.css"))
                    f.write('<!DOCTYPE HTML>'
                            '<HTML>'
                            '<HEAD><LINK rel="stylesheet" href="styles.css" type="text/css">'
                            '</HEAD>')
                    for page in html_list:
                        f.write(f'<a href="{page.name}">{page.name[:-5]}</a><br>')
                    f.write('</HTMl>')

                progress_label.setText("HTML collation finished")
                QtWidgets.QApplication.processEvents()


        self.load_dialog.close()

