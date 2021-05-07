from PySide2 import QtWidgets, QtGui

class ReplaceActionHandler():
    """A function that stores a QAction and a function to send the action to as a parameter to when the action is triggered"""

    def __init__(self, action: QtWidgets.QAction, trigger_func):
        print("init")
        self.action = action
        self.action.triggered.connect(self.invoke_trigger)
        self.trigger_func = trigger_func

    def invoke_trigger(self):
        print("invoked")
        self.trigger_func(self.action)

