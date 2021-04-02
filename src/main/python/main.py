import mistune
from fbs_runtime.application_context.PySide2 import ApplicationContext
from ViewPane import ViewPane
from EditPane import EditPane
import sys
import regex
import random
from PySide2 import QtCore, QtWidgets, QtGui
import json
import os
from enum import Enum

import highlighter


class AppContext(ApplicationContext):
    def run(self):                              # 2. Implement run()
        mainPane = MainPane()
        mainPane.resize(800, 600)
        mainPane.show()
        version = self.build_settings['version']
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
        self.viewPane.setMaximumWidth(self.width()*0.5)
        self.viewPane.setMinimumWidth(self.width()*0.5)
        self.setContentsMargins(self.width() * 0.25, 0, self.width() * 0.25, 0)
        self.buttonSwitchPane = QtWidgets.QPushButton("Switch Pane")
        self.buttonSwitchPane.clicked.connect(self.switchPane)
        self.setStyleSheet(stylesheet)



        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.editPane)
        self.layout.addWidget(self.viewPane)
        self.layout.addWidget(self.buttonSwitchPane)

    def resizeEvent(self, event:QtGui.QResizeEvent) -> None:
        print("Woo")
        self.setContentsMargins(self.width() * 0.25, 0, self.width() * 0.25, 0)
        self.viewPane.setMaximumWidth(self.width()*0.5)
        html = regex.sub(r'(?<=<img[^>]*)(width="[\d.]+")', f'width="{self.viewPane.width()}" ', self.viewPane.toHtml())
        self.viewPane.setHtml(html)
        print(self.editPane.font())


    def switchPane(self):
        self.editPane.setVisible(not self.editPane.isVisible())
        self.viewPane.setHtml(mistune.markdown(self.editPane.toPlainText(), renderer=highlighter.HighlightRenderer()))
        self.viewPane.setMaximumWidth(self.width()*0.5)
        self.viewPane.setMinimumWidth(self.width()*0.5)
        html = self.viewPane.toHtml().replace("<img ", f'<img width="{self.viewPane.width()}" ')
        self.viewPane.setHtml(html)
        self.viewPane.setVisible(not self.viewPane.isVisible())


if __name__ == "__main__":
    ctx = AppContext()

    sys.exit(ctx.run())
