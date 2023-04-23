import ctypes
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication

import utils
from controllers.main_controller import MainController

os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'


class MainWindow(QMainWindow, MainController):
    def __init__(self):
        super().__init__()
        self.screenMode = False
        self.setupUi(self)
        self.setWindowIcon(utils.get_icon())
        self.video_window.fullScreenSignal.connect(self.full_screen)

    def resizeEvent(self, event):
        self.stackedWidget.setFixedSize(event.size().width(), event.size().height())
        return super().resizeEvent(event)

    # prevent screen recording
    @staticmethod
    def prevent_screen_recording():
        # platform
        if sys.platform == "win32":
            user32 = ctypes.WinDLL("user32")
            hwnd = user32.GetForegroundWindow()
            user32.SetWindowDisplayAffinity(hwnd, 1)

    def full_screen(self):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.showMaximized()
        self.screenMode = True

    def normalMode(self):
        self.screenMode = False
        self.setWindowFlags(Qt.WindowType.Window)
        self.showMaximized()
        self.video_window.control_layout_toggle(False)

    def mouseDoubleClickEvent(self, event):
        cursor_pos = QCursor.pos()
        screen_height = QApplication.primaryScreen().geometry().height()
        if cursor_pos.y() > screen_height - 200:
            if self.screenMode:
                self.normalMode()
        return super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.screenMode:
                self.normalMode()
        return super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.prevent_screen_recording()
    app.exec()
