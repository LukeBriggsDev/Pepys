"""
    Copyright (C) 2021  Luke Briggs <lukebriggs02@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

import pathlib
import typing
from threading import Thread

from PyQt6 import QtWidgets, QtGui, QtCore
from EditPane import EditPane
from datetime import date, datetime

from CONSTANTS import get_resource
from ColorParser import *
import pypandoc
from pathlib import Path
import PyPDF2
import os
import sys
import CONSTANTS
import shutil
import EntryFile

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

    def __init__(self, main_window, edit_pane: EditPane):
        super().__init__()
        # Window options
        self.main_window = main_window
        self.edit_pane = edit_pane
        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)
        self.setWindowFlag(QtCore.Qt.WindowType.Dialog)

        self.dialog_layout = QtWidgets.QVBoxLayout()

        formLayout = QtWidgets.QFormLayout()
        self.export_options = QtWidgets.QComboBox()

        # Workaround for button elements not changing BG on MacOS
        if QtWidgets.QApplication.palette().color(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base).lightness() < 122\
            and (sys.platform == "darwin" or sys.platform == "win32"):
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


        for output_format in sorted(self.output_formats.keys(), key=str.lower):
            self.export_options.addItem(output_format)
        formLayout.addRow("Export Format:", self.export_options)

        # Selecting export date
        self.date_select_layout = QtWidgets.QGridLayout()

        self.date_options = QtWidgets.QComboBox()
        self.date_options.addItems(["Current Entry", "Custom Range", "All Entries"])
        self.date_select_layout.addWidget(self.date_options, 0, 0, 2, 1)
        self.date_options.currentTextChanged.connect(self.disable_custom_date)

        self.custom_date_layout = QtWidgets.QFormLayout()

        self.start_date_widget = QtWidgets.QDateEdit()
        self.start_date_widget.setMinimumWidth(200)
        self.start_date_widget.setDisplayFormat("yyyy-MM-dd")
        self.start_date_widget.setDate(QtCore.QDate.currentDate())
        self.custom_date_layout.addRow("Start Date:", self.start_date_widget)

        self.end_date_widget = QtWidgets.QDateEdit()
        self.end_date_widget.setMinimumWidth(200)
        self.end_date_widget.setDisplayFormat("yyyy-MM-dd")
        self.end_date_widget.setDate(QtCore.QDate.currentDate())
        self.custom_date_layout.addRow("End Date:", self.end_date_widget)
        self.end_date_widget.dateChanged.connect(self.start_date_widget.setMaximumDate)
        self.start_date_widget.dateChanged.connect(self.end_date_widget.setMinimumDate)

        self.date_select_layout.addLayout(self.custom_date_layout, 2, 0, self.custom_date_layout.rowCount(), 2)
        formLayout.addRow("Select Date:", self.date_select_layout)

        # Export location
        chosen_directory_layout = QtWidgets.QHBoxLayout()
        self.chosen_directory = QtWidgets.QLabel()
        browse_button = QtWidgets.QPushButton("Browse")
        chosen_directory_layout.addWidget(browse_button)
        chosen_directory_layout.addWidget(self.chosen_directory)
        formLayout.addRow("Select Directory:", chosen_directory_layout)
        browse_button.clicked.connect(self.browse_clicked)


        self.will_collate = QtWidgets.QCheckBox()
        formLayout.addRow("Collate together (PDF, HTML only):", self.will_collate)

        self.setLayout(self.dialog_layout)
        self.dialog_layout.addLayout(formLayout)


        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.clicked.connect(self.export_clicked)
        self.dialog_layout.addWidget(self.export_button)


        self.setWindowTitle("Export")

        self.disable_custom_date()
        self.export_options.currentTextChanged.connect(self.format_option_change)
        self.format_option_change(None)

    def browse_clicked(self):
        self.file_dialog = QtWidgets.QFileDialog()
        self.chosen_directory.setText(self.file_dialog.getExistingDirectory(self, "Open Directory",
                                                                            pathlib.Path.home().as_posix(),
                                                                            QtWidgets.QFileDialog.Option.ShowDirsOnly))

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        # Re-enable main window
        self.main_window.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
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
            self.start_date_widget.setDate(date(int(self.edit_pane.current_file_date[:4]),
                                                int(self.edit_pane.current_file_date[5:7]),
                                                int(self.edit_pane.current_file_date[8:10])))
            self.end_date_widget.setDate(date(int(self.edit_pane.current_file_date[:4]),
                                              int(self.edit_pane.current_file_date[5:7]),
                                              int(self.edit_pane.current_file_date[8:10])))
        else:
            self.start_date_widget.setEnabled(True)
            self.end_date_widget.setEnabled(True)

    def export_clicked(self):
        self.export_diary()
        self.setEnabled(True)


    def export_diary(self):

        # Load dialog
        self.load_dialog = QtWidgets.QDialog(self)
        self.load_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.load_dialog.setMinimumSize(400, 100)
        self.load_dialog.setMaximumSize(400, 100)
        self.load_dialog.setWindowTitle("Exporting...")
        progress_label = QtWidgets.QLabel()
        progress_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.load_dialog.setLayout(QtWidgets.QVBoxLayout())
        self.load_dialog.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.load_dialog.layout().addWidget(progress_label)
        self.load_dialog.layout().addWidget(progress_bar)
        self.load_dialog.show()
        self.setDisabled(True)
        self.load_dialog.setEnabled(True)

        with open(get_resource("config.json"), "r") as file:
            directory = json.loads(file.read())["diary_directory"]

        if not os.path.exists(self.chosen_directory.text()):
            try:
                os.mkdir(os.path.join(Path(directory), "export"))
            except FileExistsError:
                shutil.rmtree(os.path.join(Path(directory), "export"), ignore_errors=True)
                os.mkdir(os.path.join(Path(directory), "export"))

            self.chosen_directory.setText(os.path.join(directory, "export"))

        # Custom Range
        if self.date_options.currentText() == "Custom Range":
            diary_entries = EntryFile.get_all_entry_files_in_range(self.start_date_widget.date().toPyDate(), self.end_date_widget.date().toPyDate())
        # Current Date
        elif self.date_options.currentText() == "Current Entry":
            current_date = datetime.strptime(self.edit_pane.current_file_date, "%Y-%m-%d")
            diary_entries = EntryFile.get_all_entry_files_in_range(current_date, current_date)
        else:
            diary_entries = EntryFile.get_all_entry_files()

        format = self.output_formats[self.export_options.currentText()]


        pdoc_args = ["--standalone",
                     f"--katex={get_resource('katex/')}"]

        if format["type"] == "pdf":
            # Convert to html before pdf to apply css
            pdoc_args.append("-thtml")
            if sys.platform.startswith("win32") and shutil.which("wkhtmltopdf") is None:
                pdoc_args.append(f"--pdf-engine={get_resource('wkhtmltopdf.exe')}")
            if sys.platform.startswith("darwin"):
                pdoc_args.append(f"--pdf-engine=/usr/local/bin/wkhtmltopdf")

        if format["type"] == "html" or format["type"] == "pdf":
            with open(get_resource("parsed_stylesheet.css"), "w+") as f:
                f.write(parse_stylesheet(get_resource("ViewPaneStyle.css"), "light"))
            pdoc_args.append("--css="+get_resource("HTMLExport.css"))
            pdoc_args.append("--self-contained")
            pdoc_args.append("--pdf-engine-opt=--enable-local-file-access")


        progress_label.setText("Converting to " + str(format["type"]))
        progress_bar.setMaximum(len(diary_entries))
        QtWidgets.QApplication.processEvents()
        finished = 0
        errors = []
        # Conversion
        for entry in diary_entries:
            if self.load_dialog.isVisible():
               
                has_encryption = entry.is_encrypted()
                if has_encryption:
                    entry.set_to_unencrypted()

                path = pathlib.Path(entry.directory).as_posix()
                os.chdir(path)
                try:
                    pypandoc.convert_file(entry.filename, format["type"],
                                          outputfile=(self.chosen_directory.text() + "/" + entry.filename[:-3] + "." + format["ext"]),
                                          extra_args=pdoc_args)
                except RuntimeError as err:
                    progress_label.setText("ERROR IN FILE " + entry.filename)
                    QtWidgets.QApplication.processEvents()
                    errors.append(entry)
                    print(str(err))
                    if str(err).startswith('Pandoc died with exitcode "47"'):
                        self.load_dialog.setMinimumSize(550, 150)
                        self.load_dialog.setMaximumSize(550, 150)
                        progress_bar.setVisible(False)
                        exit_button = QtWidgets.QPushButton("Close")
                        self.load_dialog.layout().addWidget(exit_button)
                        exit_button.clicked.connect(self.load_dialog.close)
                        progress_label.setText("No wkhtmltopdf installation found.\n"
                                               "Please install wkhtmltopdf.\n\n")
                        return 1
                
                if has_encryption:
                    entry.set_to_encrypted()

                finished += 1
                progress_label.setText(str(finished) + "/" + str(len(diary_entries)))
                progress_bar.setValue(finished)
                QtWidgets.QApplication.processEvents()
            else:
                return 2
        progress_label.setText("Conversion finished")
        QtWidgets.QApplication.processEvents()

        if self.will_collate.isChecked():
            # Collate pdfs together into one pdf
            if format["type"] == "pdf":
                progress_label.setText("Starting pdf collation")
                QtWidgets.QApplication.processEvents()
                file_merger = PyPDF2.PdfFileMerger(strict=False)
                pdf_list = sorted([Path(os.path.join(self.chosen_directory.text(), entry.filename[:-3] + ".pdf"))
                                   for entry in diary_entries
                                   if os.path.isfile(os.path.join(self.chosen_directory.text(), entry.filename[:-3] + ".pdf"))],
                                   key=lambda x: x.name)

                for pdf in pdf_list:
                    progress_label.setText(pdf.name)
                    QtWidgets.QApplication.processEvents()
                    file_merger.append(pdf.as_posix(), pdf.name[:-4], import_bookmarks=False)
                    try:
                        os.remove(pdf.as_posix())
                    except PermissionError:
                        pass
                file_merger.write(self.chosen_directory.text() + "/diary.pdf")
                progress_label.setText("pdf collation finished")
                QtWidgets.QApplication.processEvents()

            # Collate html together into one pdf
            if format["type"] == "html":
                progress_label.setText("Starting html collation")
                QtWidgets.QApplication.processEvents()
                html_list = sorted([Path(os.path.join(self.chosen_directory.text(), entry.filename[:-3] + ".html"))
                                    for entry in diary_entries
                                    if os.path.isfile(os.path.join(self.chosen_directory.text(), entry.filename[:-3] + ".html"))],
                                    key=lambda x: x.name)
                html = ""
                try:
                    os.mkdir(os.path.join(Path(self.chosen_directory.text()), "html_export"))
                except FileExistsError:
                    shutil.rmtree(os.path.join(Path(self.chosen_directory.text()), "html_export"), ignore_errors=True)
                    os.mkdir(os.path.join(Path(self.chosen_directory.text()), "html_export"))

                for document in html_list:
                    shutil.move(document, os.path.join(Path(self.chosen_directory.text()), "html_export", document.name))

                with open(os.path.join(Path(self.chosen_directory.text()), "html_export", "_index.html"), "w") as f:
                    shutil.copyfile(get_resource("parsed_stylesheet.css"), os.path.join(Path(self.chosen_directory.text()), "html_export", "styles.css"))
                    f.write('<!DOCTYPE HTML>'
                            '<HTML>'
                            '<HEAD><LINK rel="stylesheet" href="styles.css" type="text/css">'
                            '</HEAD>')
                    for page in html_list:
                        f.write(f'<a href="{page.name}">{page.name[:-5]}</a><br>')
                    f.write('</HTMl>')

                progress_label.setText("HTML collation finished")
                QtWidgets.QApplication.processEvents()

        print(self.chosen_directory.text())
        if len(errors) > 0:
            self.error_dialog = QtWidgets.QMessageBox()
            self.error_dialog.setText("Errors occured in the following entries and they were not converted.\n\nPerhaps they link to files that do not exist")
            if len(errors) > 10:
                self.error_dialog.setInformativeText("\n".join([str(error) for error in errors[:10]]) + "...")
            else:
                self.error_dialog.setInformativeText("\n".join([str(error) for error in errors]))
            self.error_dialog.show()
        CONSTANTS.openFolder(self.chosen_directory.text())
        self.load_dialog.close()
