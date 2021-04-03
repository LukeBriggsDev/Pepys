import sys
from enum import Enum

import mistune
import regex
from PySide2 import QtWidgets, QtGui
from fbs_runtime import PUBLIC_SETTINGS
from fbs_runtime.application_context.PySide2 import ApplicationContext

import highlighter
from EditPane import EditPane
from ViewPane import ViewPane
from CustomMenuBar import CustomMenuBar


class AppContext(ApplicationContext):
    def run(self):                              # 2. Implement run()
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/LibreCaslon/LibreCaslonText-Regular.ttf"))
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/LibreCaslon/LibreCaslonText-Bold.ttf"))
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/LibreCaslon/LibreCaslonText-Italic.ttf"))
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/IBMPlexMono/IBMPlexMono-Regular.ttf"))

        fontdb = QtGui.QFontDatabase()
        print(fontdb.families(QtGui.QFontDatabase.WritingSystem.Latin))
        print(fontdb.applicationFontFamilies(2))

        mainPane = MainPane()
        mainPane.resize(800, 600)
        mainPane.setMinimumSize(640, 480)
        mainPane.show()
        version = PUBLIC_SETTINGS['version']
        return self.app.exec_()                 # 3. End run() with this line



class Pane(Enum):
    EDIT = 1
    VIEW = 2


class MainPane(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        filename = ctx.get_resource("styles.qss")
        with open(filename, "r") as file:
            stylesheet = file.read()

        self.editPane = EditPane(ctx)


        self.viewPane = ViewPane(ctx)
        self.viewPane.setVisible(False)
        self.buttonSwitchPane = QtWidgets.QPushButton("Switch Pane")
        self.buttonSwitchPane.clicked.connect(self.switchPane)
        self.setStyleSheet(stylesheet)
        self.menuBar = CustomMenuBar()



        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.menuBar)
        self.layout.addWidget(self.editPane)
        self.layout.addWidget(self.viewPane)
        self.layout.addWidget(self.buttonSwitchPane)

    def resizeEvent(self, event:QtGui.QResizeEvent) -> None:
        self.editPane.updateSize(self.width())
        self.viewPane.updateSize(self.width())
        html = regex.sub(r'(?<=<img[^>]*)(width="[\d.]+")', f'width="{self.viewPane.width() * 0.5}" ', self.viewPane.toHtml())
        self.viewPane.setHtml(html)


    def switchPane(self):
        self.editPane.setVisible(not self.editPane.isVisible())
        self.viewPane.setHtml(mistune.markdown(self.editPane.toPlainText(), renderer=highlighter.HighlightRenderer()))
        self.editPane.updateSize(self.width())
        self.viewPane.updateSize(self.width())
        html = self.viewPane.toHtml().replace("<img ", f'<img width="{self.viewPane.width() * 0.5}" ')
        self.viewPane.setHtml(html)
        self.viewPane.setVisible(not self.viewPane.isVisible())


if __name__ == "__main__":
    ctx = AppContext()

    sys.exit(ctx.run())
