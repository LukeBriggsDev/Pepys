import json
import re


def parse_stylesheet(stylesheet_file: str, colors_file: str, config_file: str):
    with open(stylesheet_file, "r") as pane_style, open(colors_file, "r") as colors, open(config_file, "r") as config:
        colors_dict = json.loads(colors.read())
        stylesheet = pane_style.read()
        theme = json.loads(config.read())["theme"]
        for color_role in colors_dict[theme].keys():
            stylesheet = re.sub(f"%{color_role}%", colors_dict[theme][color_role], stylesheet)

    return stylesheet
