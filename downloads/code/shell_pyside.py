# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys
import logging

from PySide.QtGui import *


from avashell.shell_base import ShellBase
from avashell.utils import resource_path

_logger = logging.getLogger(__name__)


class MainWnd(QMainWindow):
    def __init__(self, shell, icon):
        super(MainWnd, self).__init__()
        self._shell = shell
        self.icon = icon
        self.context_menu = None
        self.tray_icon = None

        if not QSystemTrayIcon.isSystemTrayAvailable():
            msg = "I couldn't detect any system tray on this system."
            _logger.error(msg)
            QMessageBox.critical(None, "AvaShell", msg)
            sys.exit(1)

        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(self.icon)
        self.setWindowTitle('AvaShell')

        self.create_tray_icon(self.icon)
        self.tray_icon.show()

    def on_tray_activated(self, reason=None):
        _logger.debug("Tray icon activated.")

    def on_quit(self):
        self._shell.quit_app()

    def create_context_menu(self):
        self.quit_action = QAction("&Quit AvaShell", self, triggered=self.on_quit)

        menu = QMenu(self)
        menu.addAction(self.quit_action)
        return menu

    def create_tray_icon(self, icon):
        self.context_menu = self.create_context_menu()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(self.context_menu)
        self.tray_icon.setIcon(icon)
        self.tray_icon.activated.connect(self.on_tray_activated)


class Shell(ShellBase):
    """ Shell implementation using PySide
    """
    def __init__(self):
        super(Shell, self).__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)  # 1
        self.icon = QIcon(resource_path('res/icon.png'))
        self.menu = None
        self.wnd = MainWnd(self, self.icon)

    def quit_app(self):
        self.app.quit()

    def run(self):
        _logger.info("Shell is running...")
        self.app.exec_()


if __name__ == '__main__':
    shell = Shell()
    shell.run()

