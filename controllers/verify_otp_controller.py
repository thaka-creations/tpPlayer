from PyQt5.QtWidgets import QMessageBox, QDialog, QPushButton

import utils
from controllers import login_controller
from ui_files.verify_otp_ui import Ui_verifyOtpForm


class VerifyOtpController(Ui_verifyOtpForm):
    def __init__(self, user):
        self.user = user
        self.successful = False
        self.closeDialog = QPushButton()

    def setupUi(self, verifyOtpForm):
        super().setupUi(verifyOtpForm)
        verifyOtpForm.setWindowIcon(utils.get_icon())
        self.verifyOtpButton.clicked.connect(self.verify_otp)
        self.resendOtpButton.clicked.connect(self.resend_otp)
        self.closeDialog.clicked.connect(verifyOtpForm.close)

    # resend otp func
    def resend_otp(self):
        status_code, resp = utils.resend_otp({"send_to": self.user})
        if not status_code:
            self.display_message("Error", resp)
            return
        self.display_message("Success", resp)

    # verify otp func
    def verify_otp(self):
        code = self.otpCodeInput.text()
        if not code:
            self.display_message("Error", "Please enter your OTP code")
            return

        status_code, resp = utils.verify_otp({"send_to": self.user, "code": code})
        if not status_code:
            self.display_message("Error", resp)
            return
        self.successful = True
        self.display_message("Success", resp)

    def on_message_box_close(self):
        self.closeDialog.click()
        loginDialog = QDialog()
        loginController = login_controller.LoginController()
        loginController.setupUi(loginDialog)
        loginDialog.exec()

    # display message function
    def display_message(self, status_code, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(status_code)
        message_box.setText(message)

        if status_code == "Success":
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.setIcon(QMessageBox.Icon.Information)
            if self.successful:
                message_box.finished.connect(self.on_message_box_close)
        else:
            message_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
            message_box.setIcon(QMessageBox.Icon.Warning)

        message_box.exec()

