from __future__ import annotations
from PySide2 import QtWidgets, QtGui, QtCore
import typing
import json
from CalendarFileSelector import CalendarFileSelector
if typing.TYPE_CHECKING:
    from main import AppContext
    from EditPane import EditPane

class FavoriteButton(QtWidgets.QPushButton):
    """Button to add the current entry to the list of favorites"""
    def __init__(self, edit_pane: EditPane, ctx: AppContext):
        """Constructor
        :param edit_pane: EditPane currently being edited
        :param ctx: Current context storing global function for accessing resources
        """
        super().__init__()
        self.edit_pane = edit_pane
        self.ctx = ctx
        self.setMinimumSize(32, 32)
        self.setMinimumSize(32, 32)
        self.refresh_icon()
        self.setToolTip("Favourite")

    def mousePressEvent(self, e:QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        # Toggle favorite status
        with open(self.ctx.get_resource("config.json"), "r+") as file:
            config_dict = json.loads(file.read())
            # Currently in favorites list
            if self.edit_pane.current_file_date in config_dict["favorites"]:
                # Remove from favorites
                config_dict["favorites"].remove(self.edit_pane.current_file_date)
            else:
                # Add to favorites
                config_dict["favorites"].append(self.edit_pane.current_file_date)

            # Write changes and refresh icon
            file.seek(0)
            file.write(json.dumps(config_dict, sort_keys=True, indent=4))
            file.truncate()
            self.refresh_icon()

    def refresh_icon(self):
        with open(self.ctx.get_resource("config.json"), "r") as file:
            config_dict = json.loads(file.read())
        if self.edit_pane.current_file_date in config_dict["favorites"]:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource(self.ctx.icons["favorite_on"][self.ctx.theme])))
        else:
            self.setIcon(QtGui.QIcon(self.ctx.get_resource((self.ctx.icons["favorite_off"][self.ctx.theme]))))



