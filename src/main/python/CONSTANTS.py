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
import json
import os
import sys
import enchant
import subprocess
import pathlib
from PyQt5 import QtGui, QtWidgets, QtCore


if sys.platform == 'darwin':
    def openFolder(path):
        subprocess.Popen(['open', path])
elif sys.platform == 'linux':
    def openFolder(path):
        try:
            subprocess.Popen(['xdg-open', path])
        except FileNotFoundError:
            # When no gui file manager is installed
            pass
elif sys.platform == 'win32':
    def openFolder(path):
        subprocess.Popen(['explorer', pathlib.Path(path)])




def get_resource(filepath):
    """
    Return absolute file path when given a path relative to base resources
    :param filepath relative to /resources/base
    """
    config_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation)
    if not os.path.exists(config_dir):
        pathlib.Path(config_dir).mkdir(parents=True)
    if not os.path.isfile(os.path.join(config_dir,"config.json")):
        with open(os.path.join(config_dir, "config.json"), "w+") as file:
            file.write('''{\n
            "diary_directory": "",\n
            "favorites": [],\n
            "theme": "dark",\n
            "enable_dict": true\n
            }''')
    else:
        with open(os.path.join(config_dir, "config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            if "enable_dict" not in config_dict.keys():
                config_dict["enable_dict"] = True
                file.seek(0)
                file.write(json.dumps(config_dict, sort_keys=True, indent=4))
                file.truncate()

    user_files = ["config.json", "wordlist.txt", "parsed_stylesheet.css"]

    # Change resource directory depending on if it is running from source or running compiled
    if sys.platform == "linux" or os.path.basename(__file__) == "CONSTANTS.py":
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources", "base")
    else:
        base_path = os.path.join(os.path.dirname(__file__),"resources", "base")

    if filepath in user_files:
        base_path = config_dir


    return os.path.join(base_path, filepath)

# Load system default dictionary
spell_lang = enchant.get_default_language() if enchant.dict_exists(enchant.get_default_language()) else "en_US"
# Load spell dictionary
spell_dict = enchant.DictWithPWL(spell_lang, get_resource("wordlist.txt"))

# Load icons and themes
with open(get_resource("icons.json")) as icons:
    icons = json.loads(icons.read())

theme = "light"
with open(get_resource("colors.json")) as colors:
    colors = json.loads(colors.read())

version = "1.1.0"

light_palette = QtWidgets.QApplication.palette()
if not sys.platform.startswith("linux"):
    light_palette.setColor(QtGui.QPalette.Mid, QtGui.QColor.fromRgbF(0.85, 0.85, 0.85))
    light_palette.setColor(QtGui.QPalette.Dark, QtGui.QColor.fromRgbF(0.8, 0.8, 0.8))
    QtWidgets.QApplication.setPalette(light_palette)


class Colors:
    """
    The following code is derived from CPP code from the adwaita-qt project
    <https://github.com/FedoraQt/adwaita-qt/blob/2ea48c88286a9c3a944d12ead288e37a490f71af/src/lib/adwaita.cpp>
    /*************************************************************************
     * Copyright (C) 2020 Jan Grulich <jgrulich@redhat.com>                  *
     *               2021 Luke Briggs <lukebriggs02@gmail.com>               *
     * This program is free software; you can redistribute it and/or modify  *
     * it under the terms of the GNU General Public License as published by  *
     * the Free Software Foundation; either version 2 of the License, or     *
     * (at your option) any later version.                                   *
     *                                                                       *
     * This program is distributed in the hope that it will be useful,       *
     * but WITHOUT ANY WARRANTY; without even the implied warranty of        *
     * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
     * GNU General Public License for more details.                          *
     *                                                                       *
     * You should have received a copy of the GNU General Public License     *
     * along with this program; if not, write to the                         *
     * Free Software Foundation, Inc.,                                       *
     * 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA .        *
     *************************************************************************/
    """
    @staticmethod
    def darken(color: QtGui.QColor, amount: float=0.1):
        h, s, l, a = color.getHslF()
        lightness = l - amount if l-amount > 0 else 0
        return QtGui.QColor.fromHslF(h, s, lightness, a)

    @staticmethod
    def desaturate(color: QtGui.QColor, amount: float=0.1):
        h, s, l, a = color.getHslF()
        saturation = s - amount if s - amount > 0 else 0
        return QtGui.QColor.fromHslF(h, saturation, l, a)

    @staticmethod
    def lighten(color: QtGui.QColor, amount: float=0.1):
        h, s, l, a = color.getHslF()
        lightness = amount + l
        if lightness > 1:
            lightness = 1

        return QtGui.QColor.fromHslF(h, s, lightness, a)

    @staticmethod
    def mix(c1: QtGui.QColor, c2: QtGui.QColor, bias: float=0.5):
        def mixQreal(a, b, bias):
            return a + (b-a) * bias

        if bias <= 0:
            return c1
        elif bias >= 1:
            return c2
        
        r = mixQreal(c1.redF(), c2.redF(), bias)
        g = mixQreal(c1.greenF(), c2.greenF(), bias)
        b = mixQreal(c1.blueF(), c2.blueF(), bias)
        a = mixQreal(c1.alphaF(), c2.alphaF(), bias)
        
        return QtGui.QColor.fromRgbF(r, g, b, a)

    @staticmethod
    def transparentize(color: QtGui.QColor, amount: float):
        h, s, l, a = color.getHslF()
        alpha = a - amount if a - amount > 0 else 0
        return QtGui.QColor.fromHslF(h, s, l, alpha)

    @staticmethod
    def getDarkpalette() -> QtGui.QPalette:
        alt_palette = QtGui.QPalette()


        base_color = Colors.lighten(Colors.desaturate(QtGui.QColor("#241f31"), 1.0), 0.02)
        text_color = QtGui.QColor("white")
        bg_color = Colors.darken(Colors.desaturate(QtGui.QColor("#3d3846"), 1.0), 0.04)
        fg_color = QtGui.QColor("#eeeeec")
        selected_bg_color = Colors.darken(QtGui.QColor("#3584e4"), 0.2)
        selected_fg_color = QtGui.QColor("white")
        osd_text_color = QtGui.QColor("white")
        osd_bg_color = QtGui.QColor("black")
        shadow = Colors.transparentize(QtGui.QColor("black"), 0.9)

        backdrop_fg_color = Colors.mix(fg_color, bg_color)
        backdrop_base_color = Colors.lighten(base_color, 0.01)
        backdrop_selected_fg_color = Colors.mix(text_color, backdrop_base_color, 0.2)

        button_base_color = Colors.darken(bg_color, 0.01)

        link_color = Colors.lighten(selected_bg_color, 0.2)
        link_visited_color = Colors.lighten(selected_bg_color, 0.1)

        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Window, bg_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.WindowText, fg_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Base, base_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.AlternateBase, base_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ToolTipBase, osd_bg_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ToolTipText, osd_text_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Text, fg_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Button, button_base_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ButtonText, fg_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.BrightText, text_color)

        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Light, Colors.lighten(button_base_color))
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Midlight, Colors.mix(Colors.lighten(button_base_color), button_base_color))
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Mid, Colors.mix(Colors.darken(button_base_color), button_base_color))
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Dark, Colors.darken(button_base_color))
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Shadow, shadow)

        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Highlight, selected_bg_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.HighlightedText, selected_fg_color)

        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Link, link_color)
        alt_palette.setColor(QtGui.QPalette.All, QtGui.QPalette.LinkVisited, link_visited_color)


        insensitive_fg_color = Colors.mix(fg_color, bg_color)
        insensitive_bg_color = Colors.mix(bg_color, base_color, 0.4)

        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, insensitive_bg_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, insensitive_fg_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Base, base_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, base_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, insensitive_fg_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, insensitive_bg_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, insensitive_fg_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, text_color)

        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, Colors.lighten(insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, Colors.mix(Colors.lighten(insensitive_bg_color), insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, Colors.mix(Colors.darken(insensitive_bg_color), insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, Colors.darken(insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, shadow)

        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, selected_bg_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, selected_fg_color)

        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Link, link_color)
        alt_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.LinkVisited, link_visited_color)


        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, bg_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, backdrop_fg_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, backdrop_base_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, backdrop_base_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Text, backdrop_fg_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, button_base_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, backdrop_fg_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, text_color)

        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Light, Colors.lighten(insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, Colors.mix(Colors.lighten(insensitive_bg_color), insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, Colors.mix(Colors.darken(insensitive_bg_color), insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, Colors.darken(insensitive_bg_color))
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, shadow)

        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, selected_bg_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, backdrop_selected_fg_color)

        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Link, link_color)
        alt_palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.LinkVisited, link_visited_color)

        return alt_palette

