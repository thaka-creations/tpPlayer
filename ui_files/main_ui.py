# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

from ui_files.player import VideoWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1441, 871))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.stackedWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stackedWidget.setStyleSheet("background: white;\n"
"margin:0px;\n"
"padding:0px;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy)
        self.page.setObjectName("page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.page)
        font = QtGui.QFont()
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #5968B0;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.frame = QtWidgets.QFrame(parent=self.page)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openPlayerButton = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.openPlayerButton.setFont(font)
        self.openPlayerButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.openPlayerButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.openPlayerButton.setObjectName("openPlayerButton")
        self.verticalLayout.addWidget(self.openPlayerButton)
        self.accountButton = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.accountButton.setFont(font)
        self.accountButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.accountButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.accountButton.setObjectName("accountButton")
        self.verticalLayout.addWidget(self.accountButton)
        self.activateKeyButton = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.activateKeyButton.setFont(font)
        self.activateKeyButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.activateKeyButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.activateKeyButton.setObjectName("activateKeyButton")
        self.verticalLayout.addWidget(self.activateKeyButton)
        self.settingsButton = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.settingsButton.setFont(font)
        self.settingsButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settingsButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.settingsButton.setObjectName("settingsButton")
        self.verticalLayout.addWidget(self.settingsButton)
        self.verticalLayout_2.addWidget(self.frame)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = VideoWindow(parent=self.stackedWidget)
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_2 = QtWidgets.QFrame(parent=self.page_3)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.backButton = QtWidgets.QPushButton(parent=self.frame_2)
        self.backButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.backButton.setFont(font)
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.backButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.backButton.setObjectName("backButton")
        self.verticalLayout_4.addWidget(self.backButton)
        self.label_5 = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: #5968B0;")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.profileNameLabel = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.profileNameLabel.setFont(font)
        self.profileNameLabel.setStyleSheet("color: black;")
        self.profileNameLabel.setObjectName("profileNameLabel")
        self.verticalLayout_4.addWidget(self.profileNameLabel)
        self.profileEmailLabel = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.profileEmailLabel.setFont(font)
        self.profileEmailLabel.setStyleSheet("color: black;")
        self.profileEmailLabel.setObjectName("profileEmailLabel")
        self.verticalLayout_4.addWidget(self.profileEmailLabel)
        self.profilePhoneLabel = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.profilePhoneLabel.setFont(font)
        self.profilePhoneLabel.setStyleSheet("color: black;")
        self.profilePhoneLabel.setObjectName("profilePhoneLabel")
        self.verticalLayout_4.addWidget(self.profilePhoneLabel)
        self.logoutButton = QtWidgets.QPushButton(parent=self.frame_2)
        self.logoutButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.logoutButton.setFont(font)
        self.logoutButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.logoutButton.setStyleSheet("background: grey;\n"
"color: white;")
        self.logoutButton.setObjectName("logoutButton")
        self.verticalLayout_4.addWidget(self.logoutButton)
        self.verticalLayout_5.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(parent=self.page_3)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.viewKeyButton = QtWidgets.QPushButton(parent=self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.viewKeyButton.setFont(font)
        self.viewKeyButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.viewKeyButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.viewKeyButton.setObjectName("viewKeyButton")
        self.verticalLayout_3.addWidget(self.viewKeyButton)
        self.registeredKeyButton = QtWidgets.QPushButton(parent=self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.registeredKeyButton.setFont(font)
        self.registeredKeyButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.registeredKeyButton.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.registeredKeyButton.setObjectName("registeredKeyButton")
        self.verticalLayout_3.addWidget(self.registeredKeyButton)
        self.verticalLayout_5.addWidget(self.frame_3)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_4 = QtWidgets.QFrame(parent=self.page_4)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.backButton2 = QtWidgets.QPushButton(parent=self.frame_4)
        self.backButton2.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.backButton2.setFont(font)
        self.backButton2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.backButton2.setStyleSheet("background: #5968B0;\n"
"color: white;")
        self.backButton2.setObjectName("backButton2")
        self.verticalLayout_6.addWidget(self.backButton2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.verticalLayout_6.addItem(spacerItem)
        self.titleLabel3 = QtWidgets.QLabel(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.titleLabel3.setFont(font)
        self.titleLabel3.setStyleSheet("color: black;")
        self.titleLabel3.setObjectName("titleLabel3")
        self.verticalLayout_6.addWidget(self.titleLabel3)
        self.verticalLayout_7.addWidget(self.frame_4)
        self.keyListWidget = QtWidgets.QListWidget(parent=self.page_4)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.keyListWidget.setFont(font)
        self.keyListWidget.setStyleSheet("color: black;")
        self.keyListWidget.setObjectName("keyListWidget")
        self.verticalLayout_7.addWidget(self.keyListWidget)
        self.stackedWidget.addWidget(self.page_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tafa Player"))
        self.label.setText(_translate("MainWindow", "TAFA PLAYER"))
        self.openPlayerButton.setText(_translate("MainWindow", "OPEN PLAYER"))
        self.accountButton.setText(_translate("MainWindow", "MY ACCOUNT"))
        self.activateKeyButton.setText(_translate("MainWindow", "ACTIVATE KEY"))
        self.settingsButton.setText(_translate("MainWindow", "SETTINGS"))
        self.backButton.setText(_translate("MainWindow", "BACK"))
        self.label_5.setText(_translate("MainWindow", "PROFILE"))
        self.profileNameLabel.setText(_translate("MainWindow", "NAME:"))
        self.profileEmailLabel.setText(_translate("MainWindow", "EMAIL:"))
        self.profilePhoneLabel.setText(_translate("MainWindow", "PHONE:"))
        self.logoutButton.setText(_translate("MainWindow", "LOGOUT"))
        self.viewKeyButton.setText(_translate("MainWindow", "VIEW KEYS"))
        self.registeredKeyButton.setText(_translate("MainWindow", "VIEW KEYS REGISTERED ON OTHER DEVICES"))
        self.backButton2.setText(_translate("MainWindow", "BACK"))
        self.titleLabel3.setText(_translate("MainWindow", "TextLabel"))
