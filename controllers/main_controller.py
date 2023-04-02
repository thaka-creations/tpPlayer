import base64

from PyQt6.QtCore import QSettings
from PyQt6.QtNetwork import QNetworkAccessManager
from PyQt6.QtWidgets import QDialog

from controllers.login_controller import LoginController
from ui_files.main_ui import Ui_MainWindow
from controllers.activate_key_controller import ActivateKeyController
import utils

ss = QSettings("TafaPlayer", "TafaPlayer")


class MainController(Ui_MainWindow):
    def __init__(self):
        self.MainWindow = None
        self.nam = QNetworkAccessManager()
        self.check_internet_connection()

        if not utils.is_authenticated():
            self.redirect_to_login()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.openPlayerButton.clicked.connect(self.open_player)
        self.activateKeyButton.clicked.connect(self.activate_key)
        self.accountButton.clicked.connect(self.navigate_to_account)

    # open player button
    def open_player(self):
        self.stackedWidget.setCurrentIndex(1)


    # activate key button
    def activate_key(self):
        dialog = QDialog()
        activate_key_dialog = ActivateKeyController()
        activate_key_dialog.setupUi(dialog)
        dialog.exec()

    def navigate_to_account(self):
        try:
            name = ss.value("name")
            phone = ss.value("phone")
            name = base64.b64decode(name.encode('utf-8')).decode("utf-8")
            phone = base64.b64decode(phone.encode('utf-8')).decode("utf-8")
            username = ss.value("username")
            self.profileNameLabel.setText("NAME: " + name.title())
            self.profileEmailLabel.setText("EMAIL: " + username)
            self.profilePhoneLabel.setText("PHONE: " + phone)
        except Exception as e:
            print(e)
            utils.delete_headers()
            self.redirect_to_login()

        self.stackedWidget.setCurrentIndex(2)

    def check_internet_connection(self):
        pass

    def redirect_to_login(self):
        dialog = QDialog()
        login_dialog = LoginController()
        login_dialog.setupUi(dialog)
        dialog.exec()
