import requests
from PyQt5.QtWidgets import QMessageBox, QPushButton, QDialog

from controllers import verify_otp_controller, register_controller
from ui_files.login_ui import Ui_loginDialog
from settings import BASE_URL
import utils


class LoginController(Ui_loginDialog):
    def __init__(self, main_window=None):
        self.closeDialog = QPushButton()
        self.main_window = main_window
        self.user = None

    def setupUi(self, loginDialog):
        super().setupUi(loginDialog)
        loginDialog.setWindowIcon(utils.get_icon())
        self.loginButton.clicked.connect(self.login)
        self.createAccountButton.clicked.connect(self.redirect_to_registration)
        self.closeDialog.clicked.connect(loginDialog.close)

    # authenticate user
    def login(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        url = f"{BASE_URL}/api/v1/users/auth/login"

        if not username or not password:
            self.display_message("Error", "Please enter a username and password")
            return

        try:
            response = requests.post(url, json={"username": username, "password": password},
                                     timeout=10)
            if response.status_code == 200:
                # login successful, store headers
                utils.store_headers(response.json()['message'], password)
                self.closeDialog.click()

                # show main window if available
                if self.main_window:
                    self.main_window.show()
            else:
                resp = response.json()
                if resp.get('user'):
                    self.user = resp['user']
                self.display_message("Error", resp['message'])
        except requests.exceptions.ConnectionError:
            self.display_message("Error", "Please check your internet connection")
            return

    # redirect to verification of otp
    def redirect_to_otp_verification(self):
        self.closeDialog.click()
        verifyOtpDialog = QDialog()
        verifyOtpController = verify_otp_controller.VerifyOtpController(self.user)
        verifyOtpController.setupUi(verifyOtpDialog)

        # resend otp
        utils.resend_otp({"send_to": self.user})
        verifyOtpDialog.exec()

    # redirect to registration
    def redirect_to_registration(self):
        self.closeDialog.click()
        registerDialog = QDialog()
        registerController = register_controller.RegisterController()
        registerController.setupUi(registerDialog)
        registerDialog.exec()

    # display message function
    def display_message(self, status_code, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(status_code)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if status_code == "Success":
            message_box.setIcon(QMessageBox.Icon.Information)
        else:
            message_box.setIcon(QMessageBox.Icon.Warning)
            if bool(self.user):
                message_box.finished.connect(self.redirect_to_otp_verification)

        message_box.exec()
