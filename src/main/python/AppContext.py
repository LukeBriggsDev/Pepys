import sys
from PySide2 import QtWidgets, QtGui
from fbs_runtime import PUBLIC_SETTINGS
from fbs_runtime.application_context.PySide2 import ApplicationContext
from MainWindow import MainWindow


class AppContext(ApplicationContext):
    """Responsible for connecting to fbs."""
    def run(self) -> None:
        """Override run method to launch main_window first"""

        # Add fonts
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/Inter/Inter.ttf"))
        QtGui.QFontDatabase.addApplicationFont(ctx.get_resource("fonts/IBMPlexMono/IBMPlexMono-Regular.ttf"))


        # Initialise and set size of main_window
        main_window = MainWindow(self)
        main_window.resize(800, 600)
        main_window.setMinimumSize(640, 480)
        main_window.show()
        version = PUBLIC_SETTINGS['version']
        return self.app.exec_()


if __name__ == "__main__":
    ctx = AppContext()

    sys.exit(ctx.run())
