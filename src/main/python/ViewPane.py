from __future__ import annotations
from PySide2 import QtCore, QtWidgets, QtGui
import AbstractPane
import typing
if typing.TYPE_CHECKING:
    from AppContext import AppContext

import regex


class ViewPane(AbstractPane.AbstractPane):
    """Pane for viewing rendered markdown in."""
    def __init__(self, ctx: AppContext) -> None:
        """Initialise ViewPane.

        :param ctx: current ApplicationContext
        """
        super().__init__(ctx)
        self.setReadOnly(True)

        filename = ctx.get_resource("ViewPaneStyle.qss")
        with open(filename) as file:
            stylesheet = file.read()
        self.setStyleSheet(self.styleSheet() + stylesheet)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setEnabled(False)

    def update_size(self, new_frame_width: int) -> None:
        super(ViewPane, self).update_size(new_frame_width)
        # TODO: Make resizing large images less laggy
        html = regex.sub(r'(?<=<img[^>]*)(width="[\d.]+")', f'width="{self.width() * 0.5}" ',
                         self.toHtml())
        self.setHtml(html)




