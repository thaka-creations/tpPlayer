from ui_files.activation_dialog_ui import Ui_activateKeyDialog


class ActivateKeyController(Ui_activateKeyDialog):
    def __init__(self, main_window=None, stacked_widget=None):
        self.MainWindow = main_window
        self.stackedWidget = stacked_widget
