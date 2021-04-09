from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
import json
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from AppContext import AppContext
    from EditPane import EditPane

class FavoriteButton(QtWidgets.QPushButton):
    def __init__(self, edit_pane: EditPane, ctx: AppContext):
        super().__init__()
        self.edit_pane = edit_pane
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.refresh_icon()
        self.setToolTip("Favourite")


    def update_favorite(self):
        # TODO: abstract this out along with the other icons
        with open(self.ctx.get_resource("config.json"), "r") as file, open(self.ctx.get_resource("config.json"), "r") as config:
            if self.edit_pane.current_file_date in json.loads(file.read())["favorites"]:
                self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["favorite_on"][self.ctx.theme])))
            else:
                self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["favorite_off"][self.ctx.theme])))


    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        with open(self.ctx.get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
            if self.edit_pane.current_file_date in config_dict["favorites"]:
                config_dict["favorites"].remove(self.edit_pane.current_file_date)
                self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["favorite_off"][self.ctx.theme])))
            else:
                config_dict["favorites"].append(self.edit_pane.current_file_date)
                self.setIcon(QtGui.QIcon(self.ctx.get_resource((self.ctx.icons["favorite_on"][self.ctx.theme]))))
        with open(self.ctx.get_resource("config.json"), "w") as file:
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))

    def refresh_icon(self):
        with open(self.ctx.get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
        if self.edit_pane.current_file_date in config_dict["favorites"]:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["favorite_on"][self.ctx.theme])))
        else:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource((self.ctx.icons["favorite_off"][self.ctx.theme]))))



