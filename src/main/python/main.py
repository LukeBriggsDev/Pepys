import sys
from enum import Enum

import mistune
import regex
from PySide2 import QtWidgets, QtGui
from fbs_runtime import PUBLIC_SETTINGS
from fbs_runtime.application_context.PySide2 import ApplicationContext
import os
import CodeSyntaxHighlighter
from EditPane import EditPane
from ViewPane import ViewPane
from CustomMenuBar import CustomMenuBar


class AppContext(ApplicationContext):
    def run(self):                              # 2. Implement run()
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/Inter/Inter.ttf"))
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/IBMPlexMono/IBMPlexMono-Regular.ttf"))

        fontdb = QtGui.QFontDatabase()

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
        self.menuBar = CustomMenuBar(self.editPane)



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
        self.editPane.updateSize(self.width())
        self.viewPane.updateSize(self.width())


        self.viewPane.setHtml(mistune.markdown(self.editPane.toPlainText(), renderer=CodeSyntaxHighlighter.HighlightRenderer()))
        html = self.viewPane.toHtml().replace("<img ", f'<img width="{self.viewPane.width() * 0.5}" ')
        filePathPatter = regex.compile('(?<=src=")\S*(?=")')
        filepaths = [filepath.group() for filepath in regex.finditer(filePathPatter, self.viewPane.toHtml())]

        for filepath in filepaths:
            if filepath[0] != "/" or filepath[1] != ":":
                # Replace relative file paths
                # TODO: Maybe need to make directory separators agnostic for windows
                html = html.replace(filepath, os.path.join("/".join(self.editPane.currentFile.split("/")[:-1]), filepath))


        self.viewPane.setHtml(html)
        self.viewPane.setVisible(not self.viewPane.isVisible())


if __name__ == "__main__":
    ctx = AppContext()

    sys.exit(ctx.run())
