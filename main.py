import ctypes
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication

import utils
from ui_files.main_ui import Ui_MainWindow
from controllers.main_controller import MainController


class MainWindow(QMainWindow, MainController):
    def __init__(self):
        super().__init__()
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


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.prevent_screen_recording()
    app.exec()
