from PyQt5.QtWidgets import QMessageBox, QDialog

import utils
from PyQt5.QtCore import QSettings

from controllers import login_controller
from ui_files.activation_dialog_ui import Ui_activateKeyDialog


class ActivateKeyController(Ui_activateKeyDialog):

    def __init__(self, main_window=None, stacked_widget=None):
        self.MainWindow = main_window
        self.stackedWidget = stacked_widget

    def setupUi(self, activateKeyDialog):
        super().setupUi(activateKeyDialog)
        self.activateKeyButton.clicked.connect(self.activate_key)
        self.cancelKeyDialogButton.clicked.connect(activateKeyDialog.close)

    def activate_key(self):
        key = self.keyInputEdit.text()
        ss = QSettings("TafaPlayer", "TafaPlayer")
        username = ss.value("username")
        password = ss.value("password")
        headers = {"username": username, "password": password}

        try:
            app_id = utils.get_app_id()['id']
        except Exception as e:
            app_id = None
            print(e)
            if not utils.register_app():
                self.display_message("Error", "Restart application")
                return
            else:
                self.activate_key()

        if not key:
            self.display_message("Error", "Please enter a key")
            return

        if not app_id:
            self.display_message("Error", "Restart application")
            return
        status_code, message = utils.activate_key(key, app_id, headers)

        if not status_code:
            if message == '403':
                utils.delete_headers()
                self.redirect_to_login()
            else:
                self.display_message("Error", message)
            return

        utils.register_keys(message)
        self.display_message("Success", "Key Activated Successfully")

    def display_message(self, status_code, message):
        self.cancelKeyDialogButton.click()
        message_box = QMessageBox()
        message_box.setWindowTitle(status_code)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if status_code == "Success":
            message_box.setIcon(QMessageBox.Icon.Information)
        else:
            message_box.setIcon(QMessageBox.Icon.Warning)

        message_box.exec()

    def redirect_to_login(self):
        # close main window
        self.stackedWidget.setCurrentIndex(0)
        self.MainWindow.close()

        # del headers
        utils.delete_headers()
        dialog = QDialog()
        login_dialog = login_controller.LoginController(self.MainWindow)
        login_dialog.setupUi(dialog)
        dialog.exec()
