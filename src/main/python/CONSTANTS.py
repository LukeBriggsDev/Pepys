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

