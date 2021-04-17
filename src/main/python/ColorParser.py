import json
import re


def parse_stylesheet(stylesheet_file_path: str, colors_file_path: str, config_file_path: str) -> str:
    """Parses stylesheet files with logical formatting to a readable form
    :param stylesheet_file_path: path to the stylesheet file to parse
    :param colors_file_path: path to file containing mapping of logical colours to rgb
    :param config_file_path: path to config file storing the current theme
    :return stylesheet as a string
    """
    with open(stylesheet_file_path, "r") as pane_style, open(colors_file_path, "r") as colors, open(config_file_path, "r") as config:
        colors_dict = json.loads(colors.read())
        stylesheet = pane_style.read()
        theme = json.loads(config.read())["theme"]
        for color_role in colors_dict[theme].keys():
            stylesheet = re.sub(f"%{color_role}%", colors_dict[theme][color_role], stylesheet)

    return stylesheet
