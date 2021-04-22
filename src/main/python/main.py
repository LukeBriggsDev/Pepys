import sys
from PySide2 import QtWidgets, QtGui
from MainWindow import MainWindow
import os
import json


class AppContext:
    """Used to store global variables and functions"""
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        # Add fonts
        fonts = ["Inter/Inter-Black.ttf",
                 "Inter/Inter-Bold.ttf",
                 "Inter/Inter-ExtraBold.ttf",
                 "Inter/Inter-Light.ttf",
                 "Inter/Inter-Medium.ttf",
                 "Inter/Inter-Regular.ttf",
                 "Inter/Inter-SemiBold.ttf",
                 "Inter/Inter-Thin.ttf",
                 "RobotoMono/RobotoMono-Bold.ttf",
                 "RobotoMono/RobotoMono-BoldItalic.ttf",
                 "RobotoMono/RobotoMono-ExtraLight.ttf",
                 "RobotoMono/RobotoMono-ExtraLightItalic.ttf",
                 "RobotoMono/RobotoMono-Italic.ttf",
                 "RobotoMono/RobotoMono-Light.ttf",
                 "RobotoMono/RobotoMono-LightItalic.ttf",
                 "RobotoMono/RobotoMono-Medium.ttf",
                 "RobotoMono/RobotoMono-MediumItalic.ttf",
                 "RobotoMono/RobotoMono-Regular.ttf",
                 "RobotoMono/RobotoMono-SemiBold.ttf",
                 "RobotoMono/RobotoMono-SemiBoldItalic.ttf",
                 "RobotoMono/RobotoMono-Thin.ttf",
                 "RobotoMono/RobotoMono-ThinItalic.ttf"]

        [QtGui.QFontDatabase.addApplicationFont(self.get_resource("fonts/" + font)) for font in fonts]

        # Load icons and themes
        with open(self.get_resource("icons.json")) as icons:
            self.icons = json.loads(icons.read())
        with open(self.get_resource("config.json")) as config:
            self.theme = json.loads(config.read())["theme"]
        with open(self.get_resource("colors.json")) as colors:
            self.colors = json.loads(colors.read())

        #Initialise and set size of main_window
        self.main_window = MainWindow(self)
        self.main_window.resize(800, 600)
        self.main_window.setMinimumSize(640, 480)
        self.main_window.show()
        self.version = "0.1.0"



    def run(self):
        return self.app.exec_()

    def get_resource(self, filepath):
        """
        Return absolute file path when given a path relative to base resources
        :param filepath relative to /resources/base
        """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.dirname(__file__))

        return base_path + "/resources/base/" + filepath

if __name__ == "__main__":
    print(os.path.dirname(__file__))
    ctx = AppContext()

    sys.exit(ctx.run())
