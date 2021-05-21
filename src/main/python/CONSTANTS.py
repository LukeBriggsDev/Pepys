import json
import os
import sys
import enchant
import pathlib
from PyQt5 import QtGui, QtWidgets

def get_resource(filepath):
    """
    Return absolute file path when given a path relative to base resources
    :param filepath relative to /resources/base
    """
    if not os.path.exists(pathlib.Path.home().as_posix() + "/.pepys"):
        os.mkdir(pathlib.Path.home().as_posix() + "/.pepys")
    if not os.path.isfile(pathlib.Path.home().as_posix()+"/.pepys/config.json"):
        with open(pathlib.Path.home().as_posix()+"/.pepys/config.json", "w+") as file:
            file.write('''{\n
            "diary_directory": "",\n
            "favorites": [],\n
            "theme": "dark"\n
            }''')
    user_files = ["config.json", "wordlist.txt", "parsed_stylesheet.css"]
    try:
        base_path = sys._MEIPASS + "/resources/base/"
    except Exception:
        base_path = os.path.dirname(os.path.dirname(__file__)) + "/resources/base/"

    if filepath in user_files:
        base_path = pathlib.Path.home().as_posix() + "/.pepys/"

    return base_path + filepath

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

version = "0.2.2"

light_palette = QtWidgets.QApplication.palette()

class Colors:
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
        if color.getRgb() == (40, 40, 40, 255):
            print("HSLA: ", (h, s, l, a))
        lightness = amount + l
        if lightness > 1:
            lightness = 1

        print ("lightness ", lightness)

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
        print("BASE: ", Colors.lighten(Colors.desaturate(QtGui.QColor("#241f31"), 1.0), 0.02).getRgb())
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

