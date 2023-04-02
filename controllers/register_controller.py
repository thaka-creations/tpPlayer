from PyQt6.QtWidgets import QPushButton, QMessageBox, QDialog

import utils
from controllers import verify_otp_controller
from ui_files.registration_ui import Ui_registrationForm


class RegisterController(Ui_registrationForm):
    def __init__(self):
        self.closeDialog = QPushButton()
        self.user = None

    def setupUi(self, registrationForm):
        super().setupUi(registrationForm)
        registrationForm.setWindowIcon(utils.get_icon())
        self.registerUserButton.clicked.connect(self.register)
        self.redirectToLoginButton.clicked.connect(self.redirect_to_login)
        self.closeDialog.clicked.connect(registrationForm.close)

    # register user func
    def register(self):
        first_name = self.firstNameInput.text()
        last_name = self.lastNameInput.text()
        email = self.emailAddressInput.text()
        phone = self.phoneInput.text()
        password = self.passwordInput.text()
        confirm_password = self.confirmPasswordInput.text()

        if not first_name:
            self.display_message("Error", "First name is required")
            return

        if not last_name:
            self.display_message("Error", "Last name is required")
            return

        if not email:
            self.display_message("Error", "Email address is required")
            return

        if not phone:
            self.display_message("Error", "Phone number is required")
            return

        if not password:
            self.display_message("Error", "Password is required")
            return

        if not confirm_password:
            self.display_message("Error", "Confirm password is required")
            return

        if password != confirm_password:
            self.display_message("Error", "Passwords do not match")
            return

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "password": password,
            "confirm_password": confirm_password
        }

        status_code, response = utils.register_user(payload)
        if not status_code:
            self.display_message("Error", response)
            return

        self.user = response
        self.display_message("Success", "Successfully registered. Otp has been sent to your phone")

    def on_message_box_close(self):
        self.closeDialog.click()
        verifyOtpDialog = QDialog()
        verifyOtpController = verify_otp_controller.VerifyOtpController(self.user)
        verifyOtpController.setupUi(verifyOtpDialog)
        verifyOtpDialog.exec()

    def redirect_to_login(self):
        self.closeDialog.click()
        loginDialog = QDialog()
        from controllers import login_controller
        loginController = login_controller.LoginController()
        loginController.setupUi(loginDialog)
        loginDialog.exec()

    def display_message(self, status_code, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(status_code)
        message_box.setText(message)

        if status_code == "Success":
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.finished.connect(self.on_message_box_close)
        else:
            message_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
            message_box.setIcon(QMessageBox.Icon.Warning)

        message_box.exec()
