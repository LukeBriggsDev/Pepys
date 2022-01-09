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

import typing

from PyQt6 import QtWidgets, QtGui, QtCore

from ColorParser import *

from EditPane import EditPane

if typing.TYPE_CHECKING:
    pass
import CONSTANTS
from CONSTANTS import get_resource


class SettingsWindow(QtWidgets.QWidget):
    """Window showing basic info, licenses, and version"""
    def __init__(self, main_window, edit_pane: EditPane):
        """Constructor
        :param main_window:
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.main_window = main_window
        self.setWindowFlag(QtCore.Qt.WindowType.Dialog)
        self.about_label = QtWidgets.QLabel()

        # Link settings
        self.about_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.about_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.about_label.setOpenExternalLinks(True)

        #Formatting
        self.about_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.about_label.setWordWrap(True)
        self.about_label.setText(
            f'<img src="{get_resource("icons/appicons/hires/128x128/apps/dev.lukebriggs.pepys.png")}"/>'
            '<p style="font-size: 11pt">'
            '<b>Pepys:</b><br>'
            'A Straightforward Markdown Journal<br><br>'
            '<a style="text-decoration: none; color: rgb(0,125,225);" '
            'href="https://pandoc.org/MANUAL.html#pandocs-markdown">Syntax Documentation</a><br><br>'
            '<a style="text-decoration: none; color: rgb(0,125,225);" '
            '   href="https://lukebriggs.dev">©Luke Briggs</a><br>'
            '</p>'
            f'version {CONSTANTS.version}'
            '</p>'

        )
        formLayout = QtWidgets.QFormLayout()

        formLayout.addRow(self.about_label)

        self.license_button = QtWidgets.QPushButton("Licenses")
        self.license_button.setStyleSheet("margin-bottom: 16px; height: 24px")
        self.license_button.clicked.connect(self.license_clicked)
        formLayout.addRow(self.license_button)

        self.spell_checkbox = QtWidgets.QCheckBox()
        with open(get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
            self.spell_checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked if not config_dict["enable_dict"] else QtCore.Qt.CheckState.Checked)

        self.flat_structure_checkbox = QtWidgets.QCheckBox()
        with open(get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
            check_state = QtCore.Qt.CheckState.Unchecked
            if ("use_flat_directory_structure" in config_dict) and config_dict["use_flat_directory_structure"]:
                check_state = QtCore.Qt.CheckState.Checked
        self.flat_structure_checkbox.setCheckState(check_state)

        self.spell_checkbox.stateChanged.connect(self.change_spellcheck)
        self.flat_structure_checkbox.stateChanged.connect(self.change_flat_structure)
        settings_label = QtWidgets.QLabel("Settings")
        settings_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        formLayout.addRow(settings_label)
        formLayout.addRow(QtWidgets.QLabel("Enable spell checker: "), self.spell_checkbox)
        formLayout.addRow(QtWidgets.QLabel("Use flat directory structure: "), self.flat_structure_checkbox)
       
        self.setLayout(formLayout)


        self.setStyleSheet("""    
        text-align: center;
        background-color: palette(window);
        color: palette(text);
    """)
        self.setWindowTitle("About")


    def change_spellcheck(self, state):
        CHECKED = 2
        # save state
        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            config_dict["enable_dict"] = True if state == CHECKED else False

            # Write changes and refresh icon
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()

    def change_flat_structure(self, state):
        CHECKED = 2
        # save state
        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            config_dict["use_flat_directory_structure"] = True if state == CHECKED else False

            # Write changes and refresh icon
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        self.main_window.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.main_window.setDisabled(False)
        self.edit_pane.markdownHighlighter.rehighlight()

    def license_clicked(self):
        self.license_window = QtWidgets.QTextBrowser()
        self.license_window.setFixedSize(600, 600)
        self.license_window.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont))
        self.license_window.setStyleSheet("background-color: palette(base); border: 0px solid white;")

        license_text ="""
All of the source code to this product is available under licenses which are both free and open source. 
Most of the code is available under the GNU General Public License 3.0, the licenses of included software, as well as 
that of the main software is listed below.
            """

        with open(get_resource("licenses/gpl-3.0.txt")) as file:
            license_text += '\n\nLicense used by main source available at <https://github.com/LukeBriggsDev/Pepys>' \
                            'as well as PyQt5 <https://www.riverbankcomputing.com/static/Docs/PyQt5/>\n\n'
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/num2words_license.txt")) as file:
            license_text += "License used by python library num2words <https://github.com/savoirfairelinux/num2words>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/pandoc_license.txt")) as file:
            license_text += "License used by pandoc binary <https://github.com/jgm/pandoc>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/pyenchant_license.txt")) as file:
            license_text += "License used by python library pyenchant <https://github.com/pyenchant/pyenchant>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/pypandoc_LICENSE.txt")) as file:
            license_text += "License used by python library pypandoc <https://github.com/bebraw/pypandoc>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/pypdf4_license.txt")) as file:
            license_text += "License used by python library PyPDF4 <https://github.com/claird/PyPDF4>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/pyyaml_license.txt")) as file:
            license_text += "License used by python library pyYAML <https://github.com/yaml/pyyaml>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/regex_license.txt")) as file:
            license_text += "License used by python library regex <https://bitbucket.org/mrabarnett/mrab-regex>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/setproctitle_license.txt")) as file:
            license_text += "License used by python library setproctitle <https://github.com/dvarrazzo/py-setproctitle>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/wkhtmltopdf_license.txt")) as file:
            license_text += "License used by wkhtmltopdf binary <https://github.com/wkhtmltopdf/wkhtmltopdf>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        with open(get_resource("licenses/cryptography_license.txt")) as file:
            license_text += "License used by python library cryptography <https://github.com/pyca/cryptography>\n\n"
            license_text += file.read() + "\n\n=============================================================================\n\n"

        self.license_window.setText(license_text)
        self.license_window.show()


