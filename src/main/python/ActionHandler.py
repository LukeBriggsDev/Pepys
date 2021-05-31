from PyQt5 import QtWidgets, QtGui

class ActionHandler():
    """A function that stores a QAction and a function to send the action to as a parameter to when the action is triggered"""
    def __init__(self, action: QtWidgets.QAction, trigger_func):
        self.action = action
        self.action.triggered.connect(self.invoke_trigger)
        self.trigger_func = trigger_func

    def invoke_trigger(self):
        self.trigger_func(self.action)

