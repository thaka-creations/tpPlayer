# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activationdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_activateKeyDialog(object):
    def setupUi(self, activateKeyDialog):
        activateKeyDialog.setObjectName("activateKeyDialog")
        activateKeyDialog.setWindowModality(QtCore.Qt.WindowModal)
        activateKeyDialog.resize(600, 300)
        activateKeyDialog.setMaximumSize(QtCore.QSize(600, 300))
        activateKeyDialog.setAutoFillBackground(False)
        activateKeyDialog.setStyleSheet("background: white;\n"
"color: black;")
        self.verticalLayoutWidget = QtWidgets.QWidget(activateKeyDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 551, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widget.setObjectName("widget")
        self.keyInputEdit = QtWidgets.QLineEdit(self.widget)
        self.keyInputEdit.setGeometry(QtCore.QRect(10, 20, 531, 91))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(18)
        self.keyInputEdit.setFont(font)
        self.keyInputEdit.setAutoFillBackground(False)
        self.keyInputEdit.setStyleSheet("color: black;\n"
"border: 1px solid grey;")
        self.keyInputEdit.setText("")
        self.keyInputEdit.setDragEnabled(True)
        self.keyInputEdit.setObjectName("keyInputEdit")
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(20, 1, 20, 1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cancelKeyDialogButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(24)
        self.cancelKeyDialogButton.setFont(font)
        self.cancelKeyDialogButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelKeyDialogButton.setStyleSheet("color: white;\n"
"background: #d9534f;")
        self.cancelKeyDialogButton.setObjectName("cancelKeyDialogButton")
        self.horizontalLayout_3.addWidget(self.cancelKeyDialogButton)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.activateKeyButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(24)
        self.activateKeyButton.setFont(font)
        self.activateKeyButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.activateKeyButton.setStyleSheet("color: white;\n"
"background:#5cb85c;")
        self.activateKeyButton.setObjectName("activateKeyButton")
        self.horizontalLayout_3.addWidget(self.activateKeyButton)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(activateKeyDialog)
        QtCore.QMetaObject.connectSlotsByName(activateKeyDialog)

    def retranslateUi(self, activateKeyDialog):
        _translate = QtCore.QCoreApplication.translate
        activateKeyDialog.setWindowTitle(_translate("activateKeyDialog", "Activate Key"))
        self.keyInputEdit.setPlaceholderText(_translate("activateKeyDialog", "Enter activation key"))
        self.cancelKeyDialogButton.setText(_translate("activateKeyDialog", "CANCEL"))
        self.activateKeyButton.setText(_translate("activateKeyDialog", "ACTIVATE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    activateKeyDialog = QtWidgets.QDialog()
    ui = Ui_activateKeyDialog()
    ui.setupUi(activateKeyDialog)
    activateKeyDialog.show()
    sys.exit(app.exec_())
