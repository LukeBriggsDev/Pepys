from PySide2 import QtWidgets, QtGui, QtCore
from EditPane import EditPane

class FileMenu(QtWidgets.QMenu):
    def __init__(self, editPane: EditPane):
        super().__init__("File")
        self.editPane = editPane
        newFileAction = self.addAction("New")
        newFileAction.triggered.connect(self.newFile)


        openFileAction = self.addAction("Open")
        openFileAction.triggered.connect(self.openFile)


        saveFileAction = self.addAction("Save")
        saveFileAction.triggered.connect(self.saveFile)



    def newFile(self):
        print("NewFile")

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self)
        with open(filename[0], 'r') as file:
            self.editPane.setText(file.read())
            self.editPane.applyFormatting()
            self.editPane.setCurrentFile(filename[0])


        print("OpenFile")


    def saveFile(self):
        print("SaveFile")
