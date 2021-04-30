import json
import os
import sys


def get_resource(filepath):
    """
    Return absolute file path when given a path relative to base resources
    :param filepath relative to /resources/base
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(__file__))

    return base_path + "/resources/base/" + filepath


# Load icons and themes
with open(get_resource("icons.json")) as icons:
    icons = json.loads(icons.read())
with open(get_resource("config.json")) as config:
    theme = json.loads(config.read())["theme"]
with open(get_resource("colors.json")) as colors:
    colors = json.loads(colors.read())

version = "0.2.2"

