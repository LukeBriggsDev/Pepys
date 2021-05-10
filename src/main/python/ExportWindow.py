from __future__ import annotations

import typing

from PySide2 import QtWidgets, QtGui

from CONSTANTS import get_resource
from ColorParser import *
import pypandoc
from pathlib import Path
import PyPDF4
import os
import CONSTANTS

if typing.TYPE_CHECKING:
    pass


class ExportWindow(QtWidgets.QWidget):
    """Window for selecting export options"""

    output_formats = {
        "Word Document": "docx",
        "EBook": "epub",
        "HTML": "html",
        "PDF": "pdf",
        "Latex": "latex",
        "OpenOffice Text Document": "odt",
        "Plain Text": "plain",
        "PowerPoint Slide Show": "pptx",
        "Rich Text Format": "rtf",
        "reStructuredText": "rst",
    }

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setMaximumSize(640, 240)
        self.setMinimumSize(640, 240)
        self.setWindowFlag(QtGui.Qt.Dialog)
        self.setLayout(QtWidgets.QGridLayout())

        self.export_options = QtWidgets.QComboBox()
        self.export_options.setFixedWidth(240)

        for output_format in sorted(self.output_formats.keys(), key=str.lower):
            self.export_options.addItem(output_format)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.export_label = QtWidgets.QLabel("Export Format")
        self.layout().addWidget(self.export_label, 0, 0)
        self.layout().addWidget(self.export_options,0, 1, 1, 5)

        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.clicked.connect(self.export_diary)
        self.layout().addWidget(self.export_button)

        self.setStyleSheet(parse_stylesheet(get_resource("styles.qss"), get_resource("colors.json"), get_resource("config.json")))

        self.setWindowTitle("Export")


    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        # Re-enable main window
        self.main_window.setFocusPolicy(QtGui.Qt.StrongFocus)
        self.main_window.setDisabled(False)

    def export_diary(self):
        with open(get_resource("config.json"), "r") as file:
            directory = json.loads(file.read())["diary_directory"]

        diary_entries = list(Path(directory).rglob("*.[mM][dD]"))
        format = self.output_formats[self.export_options.currentText()]

        pdoc_args = ["--standalone",
                     f"--katex={get_resource('katex/')}"]

        if format == "pdf":
            # Convert to html before pdf to apply css
            pdoc_args.append("-thtml")

        if format == "html" or format=="pdf":
            parse_stylesheet(get_resource("ViewPaneStyle.css"), get_resource("colors.json"), get_resource("config.json"))
            pdoc_args.append("--css="+get_resource("parsed_stylesheet.css"))
            pdoc_args.append("--self-contained")


        print(format)
        finished = 0
        # Conversion
        for entry in diary_entries:
            os.chdir(entry.parent.as_posix())
            try:
                pypandoc.convert_file(entry.as_posix(), format,
                                      outputfile=(entry.parent.as_posix() + "/" + entry.name[:-3] + "." + format),
                                      extra_args=pdoc_args)
            except RuntimeError as err:
                print("ERROR IN FILE " + entry.name)
                print(err)
            finished += 1
            print(str(finished) + "/" + str(len(diary_entries)))
        print("Conversion finished")

        # Collate pdfs together into one pdf
        if format == "pdf":
            print("Starting pdf collation")
            file_merger = PyPDF4.PdfFileMerger(strict=False)
            pdf_list = sorted(list(Path(directory).rglob("*-*-*.[pP][dD][fF]")), key=lambda x: x.name)
            for pdf in pdf_list:
                print(pdf.name)
                file_merger.append(pdf.as_posix(), pdf.name[:-4])
            file_merger.write(directory + "/diary.pdf")
            print("pdf collation finished")





