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
from Crypto import generateVerificationStringFromPassword, Crypto
from EntryFile import get_all_entry_files, EntryFile

if typing.TYPE_CHECKING:
    pass
import CONSTANTS
from CONSTANTS import get_resource


class SettingsWindow(QtWidgets.QDialog):
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

        with open(get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())

        self.spell_checkbox = QtWidgets.QCheckBox()
        self.spell_checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked if not config_dict["enable_dict"] else QtCore.Qt.CheckState.Checked)
        self.spell_checkbox.stateChanged.connect(self.change_spellcheck)

        self.flat_structure_checkbox = QtWidgets.QCheckBox()
        check_state = QtCore.Qt.CheckState.Unchecked
        if ("use_flat_directory_structure" in config_dict) and config_dict["use_flat_directory_structure"]:
            check_state = QtCore.Qt.CheckState.Checked
        self.flat_structure_checkbox.setCheckState(check_state)
        self.flat_structure_checkbox.stateChanged.connect(self.change_flat_structure)

        self.button_setup_encryption = QtWidgets.QPushButton("Setup Encryption")
        self.button_setup_encryption.clicked.connect(self.setup_encryption)

        self.encryption_default_checkbox = QtWidgets.QCheckBox()
        encryption_default_state = QtCore.Qt.CheckState.Unchecked
        if ("encrypt_as_default" in config_dict) and config_dict["encrypt_as_default"]:
            encryption_default_state = QtCore.Qt.CheckState.Checked
        self.encryption_default_checkbox.setCheckState(encryption_default_state)
        self.encryption_default_checkbox.stateChanged.connect(self.change_encryption_default)

        self.button_encrypt_everything = QtWidgets.QPushButton("Encrypt everything")
        self.button_encrypt_everything.clicked.connect(self.encrypt_everything)

        self.button_decrypt_everything = QtWidgets.QPushButton("Decrypt everything")
        self.button_decrypt_everything.clicked.connect(self.decrypt_everything)

        settings_label = QtWidgets.QLabel("Settings")
        settings_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        formLayout.addRow(settings_label)
        formLayout.addRow(QtWidgets.QLabel("Enable spell checker: "), self.spell_checkbox)
        formLayout.addRow(QtWidgets.QLabel("Use flat directory structure: "), self.flat_structure_checkbox)
        formLayout.addRow(QtWidgets.QLabel("Encryption: "), self.button_setup_encryption)
        formLayout.addRow(QtWidgets.QLabel("Encrypt new diary entries as default: "), self.encryption_default_checkbox)
        formLayout.addRow(QtWidgets.QLabel("Encrypt all diary entries: "), self.button_encrypt_everything)
        formLayout.addRow(QtWidgets.QLabel("Decrypt all diary entries: "), self.button_decrypt_everything)

        self.setLayout(formLayout)

        self.setStyleSheet("""    
        text-align: center;
        background-color: palette(window);
        color: palette(text);
    """)
        self.setWindowTitle("About")
        self.refresh_buttons()


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

    def setup_encryption(self):
        ret = QtWidgets.QMessageBox.question(self, "Setup encryption", """
        If you setup encryption you can optionally encrypt diary entries with a password. In this case Pepys asks you about your password on startup.
        
        The password is not stored anywhere and cannot be recovered if you forget it. So remember it well, otherwise your diary entries are lost!

        Do you want to proceed?
        """, QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if ret == QtWidgets.QMessageBox.StandardButton.No:
            return

        password, ok = QtWidgets.QInputDialog.getText(self, "Select Password", "Enter your encryption password: ", QtWidgets.QLineEdit.EchoMode.Password)
        if not ok or not password:
            return

        password_repeat, ok = QtWidgets.QInputDialog.getText(self, "Repeat Password", "Reapeat password: ", QtWidgets.QLineEdit.EchoMode.Password)
        if not ok or not password_repeat:
            return
       
        if password != password_repeat:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match", QtWidgets.QMessageBox.StandardButton.Ok)
            return

        hash = generateVerificationStringFromPassword(password)

        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            config_dict["password_hash"] = hash

            # Write changes
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()

        c = Crypto(password)
        self.button_setup_encryption.setEnabled(False)

    def change_encryption_default(self, state):
        CHECKED = 2
        # save state
        with open(get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            config_dict["encrypt_as_default"] = True if state == CHECKED else False

            # Write changes
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()

    def encrypt_everything(self):
        ret = QtWidgets.QMessageBox.question(self, "Encrypt all files", """
        This will encrypt all diary entries.
        Do you want to proceed?
        """, QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if ret == QtWidgets.QMessageBox.StandardButton.No:
            return

        files = get_all_entry_files()
        for file in files:
            if not file.is_encrypted():
                file.set_to_encrypted()

    def decrypt_everything(self):
        ret = QtWidgets.QMessageBox.question(self, "Decrypt all files", """
        This will corvert all diary entries to unencrypted markdown files.
        Do you want to proceed?
        """, QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if ret == QtWidgets.QMessageBox.StandardButton.No:
            return

        files = get_all_entry_files()
        for file in files:
            if file.is_encrypted():
                file.set_to_unencrypted()

    def refresh_buttons(self):
        c = Crypto()
        self.button_setup_encryption.setEnabled(not c.is_initialized())
        self.encryption_default_checkbox.setEnabled(c.is_initialized())

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


