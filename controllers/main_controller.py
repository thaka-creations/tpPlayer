import base64
from datetime import datetime
from threading import Thread

from PyQt5.QtCore import QSettings, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QDialog, QMessageBox

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

        # account page
        self.logoutButton.clicked.connect(self.logout)
        self.backButton.clicked.connect(self.navigate_to_home)
        self.viewKeyButton.clicked.connect(self.navigate_to_local_keys)
        self.registeredKeyButton.clicked.connect(self.fetch_online_keys)

        # keys page
        self.backButton2.clicked.connect(self.navigate_to_account)

    # open player button
    def open_player(self):
        self.stackedWidget.setCurrentIndex(1)

    # logout user
    def logout(self):
        utils.delete_headers()
        self.stackedWidget.setCurrentIndex(0)
        self.MainWindow.close()
        self.redirect_to_login()

    def navigate_to_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def navigate_to_local_keys(self):
        self.keyListWidget.clear()
        keys = utils.get_local_keys()
        try:
            if keys is not None or not keys:
                print("local keys found", keys)
                for key in keys:
                    self.keyListWidget.addItem(key['key'])
            else:
                self.display_message("Error", "No keys found")
        except Exception as e:
            print(e)
            self.display_message("Error", "No keys found")
        self.titleLabel3.setText("REGISTERED KEYS")
        self.stackedWidget.setCurrentIndex(3)

    # fetch online keys
    def fetch_online_keys(self):
        self.check_internet_connection(keys=True)

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

    # check internet connection
    def check_internet_connection(self, keys=False):
        if keys:
            self.nam.finished.connect(self.on_result)
        else:
            self.nam.finished.connect(self.on_alt_result)
        self.nam.get(QNetworkRequest(QUrl("https://www.google.com")))

    # internet response handler
    def on_result(self, reply):
        if not (reply.error() == QNetworkReply.NetworkError.NoError):
            self.display_message("Error", "This action requires internet connection")
            return
        status_code, message = utils.get_registered_keys()
        if not status_code:
            self.display_message("Error", message)
            return
        Thread(target=utils.sync_keys, daemon=False).start()
        self.keyListWidget.clear()
        try:
            for key in message:
                self.keyListWidget.addItem(key)
            self.stackedWidget.setCurrentIndex(3)
            self.titleLabel3.setText("REGISTERED KEYS ON OTHER DEVICES")
            del message

            # check for new version
            status, message = utils.check_for_new_version()
            if not status:
                self.display_message("Error", message)
                return
        except Exception as e:
            print(e)
            self.display_message("Error", "No keys found")

    def on_alt_result(self, reply):
        if not (reply.error() == QNetworkReply.NetworkError.NoError):
            reset = False
            next_connection_date = utils.get_next_connection_date()
            if not next_connection_date:
                reset = True
            else:
                if datetime.now().date() > datetime.strptime(next_connection_date, "%Y-%m-%d").date():
                    reset = True
            if reset:
                utils.delete_headers()
                self.stackedWidget.setCurrentIndex(0)
                self.MainWindow.close()
                self.redirect_to_login()
        else:
            utils.set_next_connection_date()
            Thread(target=utils.sync_keys, daemon=False).start()

            # check for new version
            status, message = utils.check_for_new_version()
            if not status:
                self.display_message("Error", message)
                return

    def redirect_to_login(self):
        dialog = QDialog()
        login_dialog = LoginController(self.MainWindow)
        login_dialog.setupUi(dialog)
        dialog.exec()

    # display message box
    @staticmethod
    def display_message(status_code, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(status_code)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if status_code == "Success":
            message_box.setIcon(QMessageBox.Icon.Information)
        else:
            message_box.setIcon(QMessageBox.Icon.Warning)

        message_box.exec()
