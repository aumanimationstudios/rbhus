# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusAuthMod.ui'
#
# Created: Sat Jan  3 12:27:07 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  def _fromUtf8(s):
    return s

try:
  _encoding = QtGui.QApplication.UnicodeUTF8
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindowAuth(object):
  def setupUi(self, MainWindowAuth):
    MainWindowAuth.setObjectName(_fromUtf8("MainWindowAuth"))
    MainWindowAuth.setWindowModality(QtCore.Qt.WindowModal)
    MainWindowAuth.resize(294, 116)
    self.centralwidget = QtGui.QWidget(MainWindowAuth)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.gridLayout = QtGui.QGridLayout()
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.labelUser = QtGui.QLabel(self.centralwidget)
    self.labelUser.setEnabled(True)
    self.labelUser.setObjectName(_fromUtf8("labelUser"))
    self.gridLayout.addWidget(self.labelUser, 0, 0, 1, 1)
    self.lineEditUser = QtGui.QLineEdit(self.centralwidget)
    self.lineEditUser.setObjectName(_fromUtf8("lineEditUser"))
    self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)
    self.labelPass = QtGui.QLabel(self.centralwidget)
    self.labelPass.setObjectName(_fromUtf8("labelPass"))
    self.gridLayout.addWidget(self.labelPass, 1, 0, 1, 1)
    self.lineEditPass = QtGui.QLineEdit(self.centralwidget)
    self.lineEditPass.setEchoMode(QtGui.QLineEdit.Password)
    self.lineEditPass.setObjectName(_fromUtf8("lineEditPass"))
    self.gridLayout.addWidget(self.lineEditPass, 1, 1, 1, 1)
    self.verticalLayout.addLayout(self.gridLayout)
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.verticalLayout.addItem(spacerItem)
    self.horizontalLayout_3 = QtGui.QHBoxLayout()
    self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
    self.checkBoxRememberMe = QtGui.QCheckBox(self.centralwidget)
    self.checkBoxRememberMe.setFocusPolicy(QtCore.Qt.StrongFocus)
    self.checkBoxRememberMe.setChecked(True)
    self.checkBoxRememberMe.setObjectName(_fromUtf8("checkBoxRememberMe"))
    self.horizontalLayout_3.addWidget(self.checkBoxRememberMe)
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem1)
    self.pushButton = QtGui.QPushButton(self.centralwidget)
    self.pushButton.setFocusPolicy(QtCore.Qt.StrongFocus)
    self.pushButton.setAutoDefault(False)
    self.pushButton.setObjectName(_fromUtf8("pushButton"))
    self.horizontalLayout_3.addWidget(self.pushButton)
    self.verticalLayout.addLayout(self.horizontalLayout_3)
    MainWindowAuth.setCentralWidget(self.centralwidget)

    self.retranslateUi(MainWindowAuth)
    QtCore.QMetaObject.connectSlotsByName(MainWindowAuth)

  def retranslateUi(self, MainWindowAuth):
    MainWindowAuth.setWindowTitle(_translate("MainWindowAuth", "login", None))
    self.labelUser.setText(_translate("MainWindowAuth", "username", None))
    self.labelPass.setText(_translate("MainWindowAuth", "password", None))
    self.checkBoxRememberMe.setText(_translate("MainWindowAuth", "rememberMe", None))
    self.pushButton.setText(_translate("MainWindowAuth", "login", None))
    self.pushButton.setShortcut(_translate("MainWindowAuth", "Return", None))

